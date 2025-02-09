import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  Button,
  TextField,
  Select,
  MenuItem,
  Box,
  Typography,
  IconButton,
} from "@mui/material";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import CloseIcon from "@mui/icons-material/Close";
import { enqueueSnackbar } from "notistack";
import {
  getReferences,
  postReference,
  calculateReferenceMutations,
  getReferenceCalculationMutationsStatus,
  postSample,
  postSampleMutations,
} from "../api";

const AddSampleDialog = ({ open, onClose }) => {
  const [newReferenceName, setNewReferenceName] = useState("");
  const [referenceFile, setReferenceFile] = useState(null);
  const [newSampleName, setNewSampleName] = useState("");
  const [sampleFile, setSampleFile] = useState(null);
  const [selectedReference, setSelectedReference] = useState("");
  const [references, setReferences] = useState([]);

  useEffect(() => {
    if (open) {
      getReferences().then((data) => {
        if (data) setReferences(data);
      });
    }
  }, [open]);

  const handleAddSample = () => {
    postSample(newSampleName, selectedReference, sampleFile)
      .then(() => postSampleMutations(newSampleName, sampleFile))
      .then(() => {
        enqueueSnackbar(`Sample ${newSampleName} added successfully`, {
          variant: "success",
        });
      })
      .catch(() => {
        enqueueSnackbar("Failed to add sample", { variant: "error" });
      })
      .finally(() => {
        setNewSampleName("");
        setSampleFile(null);
      });
  };

  const handleAddReference = (newReferenceName, referenceFile) => {
    if (!newReferenceName || !referenceFile) {
      enqueueSnackbar("Please provide a reference name and select a file.", {
        variant: "warning",
      });
      return;
    }
    postReference(newReferenceName)
      .then(() => {
        return calculateReferenceMutations(newReferenceName, referenceFile);
      })
      .then((promise) => {
        const statusFetcher = (promiseId) => {
          getReferenceCalculationMutationsStatus(promiseId).then((status) => {
            if (status["status"] === "PROGRESS") {
              setTimeout(() => {
                statusFetcher(promiseId);
              }, 1000);
              return;
            }
            if (status["status"] === "COMPLETED") {
              enqueueSnackbar(
                `Reference ${newReferenceName} added successfully`,
                {
                  variant: "success",
                }
              );
              return;
            }
            if (status["status"] === "FAILED") {
              enqueueSnackbar("Failed to add reference", {
                variant: "error",
              });
              return;
            }
          });
        };
        return statusFetcher(promise["promiseId"]);
      })
      .finally(() => {
        setNewReferenceName("");
        setReferenceFile(null);
        getReferences().then((data) => {
          if (data) setReferences(data);
        });
      });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle variant="h4" sx={{ textAlign: "center" }}>
        Add Sample
      </DialogTitle>
      <IconButton
        onClick={onClose}
        sx={{ position: "absolute", right: 16, top: 16 }}
      >
        <CloseIcon />
      </IconButton>
      <DialogContent>
        <Box display="flex" gap={4}>
          <Box flex={1} display="flex" flexDirection="column" gap={1.5}>
            <Typography variant="h6">Reference</Typography>
            <Typography variant="subtitle1" sx={{ mb: 0.5 }}>
              Reference name
            </Typography>
            <Select
              fullWidth
              value={selectedReference.toString() | ""}
              onChange={(e) => setSelectedReference(e.target.value)}
              disabled={references.length === 0}
            >
              {references.map((ref) => (
                <MenuItem key={ref.id} value={ref.name}>
                  {ref.name}
                </MenuItem>
              ))}
            </Select>
            <Typography variant="h6">Add new reference</Typography>
            <Typography variant="subtitle1" sx={{ mb: 0.5 }}>
              New reference name
            </Typography>
            <TextField
              fullWidth
              value={newReferenceName}
              onChange={(e) => setNewReferenceName(e.target.value)}
            />
            <Typography variant="subtitle1" sx={{ mb: 0.5 }}>
              Reference file
            </Typography>
            <Button
              variant="contained"
              component="label"
              startIcon={<AttachFileIcon />}
              fullWidth
              style={{ justifyContent: "flex-start" }}
              sx={{ textTransform: "none", padding: "4px 10px" }}
            >
              Choose reference file
              <input
                type="file"
                hidden
                onChange={(e) => setReferenceFile(e.target.files[0])}
              />
            </Button>
            {referenceFile && (
              <Typography variant="body2">{referenceFile.name}</Typography>
            )}
            <Button
              variant="contained"
              fullWidth
              onClick={() =>
                handleAddReference(newReferenceName, referenceFile)
              }
              sx={{ fontSize: "1rem", padding: "8px 14px" }}
            >
              Add reference
            </Button>
          </Box>

          <Box flex={1} display="flex" flexDirection="column" gap={1.5}>
            <Typography variant="h6">New sample</Typography>
            <Typography variant="subtitle1" sx={{ mb: 0.5 }}>
              Sample name
            </Typography>
            <TextField
              fullWidth
              value={newSampleName}
              onChange={(e) => {
                setNewSampleName(e.target.value);
              }}
            />
            <Typography variant="subtitle1" sx={{ mb: 0.5 }}>
              Sample file
            </Typography>
            <Button
              variant="contained"
              component="label"
              startIcon={<AttachFileIcon />}
              fullWidth
              style={{ justifyContent: "flex-start" }}
              sx={{ textTransform: "none", padding: "4px 10px" }}
            >
              Choose sample file
              <input
                type="file"
                hidden
                onChange={(e) => {
                  setSampleFile(e.target.files[0]);
                  e.target.value = null;
                }}
              />
            </Button>
            {sampleFile && (
              <Typography variant="body2">{sampleFile.name}</Typography>
            )}
            <Button
              variant="contained"
              fullWidth
              onClick={() =>
                handleAddSample(newSampleName, selectedReference, sampleFile)
              }
              sx={{ fontSize: "1rem", padding: "8px 14px" }}
            >
              Add sample
            </Button>
          </Box>
        </Box>
      </DialogContent>
    </Dialog>
  );
};

export default AddSampleDialog;
