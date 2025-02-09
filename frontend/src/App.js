import React, { useState, useEffect, useRef } from "react";
import { Box, Button, Typography, Stack, TableContainer } from "@mui/material";
import ThemeProviderWrapper from "./components/ThemeProviderWrapper";
import MetricsTable from "./components/MetricsTable";
import CompareMetricsTable from "./components/CompareMetricsTable";
import SampleList from "./components/SampleList";
import PipelinesVersionSelector from "./components/PipelinesVersionSelector";
import ComparePipelineVersion from "./components/ComparePipelinesVersion";
import AddSampleDialog from "./components/AddSampleDialog";
import {
  getMetrics,
  getSamples,
  compareMetricsAPI,
  startValidation,
  checkValidationStatus,
} from "./api";
import { enqueueSnackbar } from "notistack";

const App = () => {
  const [samples, setSamples] = useState([]);
  const [metrics, setMetrics] = useState([]);

  const [selectedSamples, setSelectedSamples] = useState([]);
  const [pipelineVersion, setPipelineVersion] = useState("");
  const [pipelineVersionToCompare, setPipelineVersionToCompare] = useState("");
  const [compareMetrics, setCompareMetrics] = useState(false);
  const compareMetricsRef = useRef(compareMetrics);
  const [openDialog, setOpenDialog] = useState(false);

  useEffect(() => {
    compareMetricsRef.current = compareMetrics;
  }, [compareMetrics]);

  useEffect(() => {
    getSamples().then((data) => setSamples(data));
  }, []);

  useEffect(() => {
    if (
      !pipelineVersion ||
      selectedSamples.length === 0 ||
      compareMetricsRef.current
    )
      return;

    const fetchMetrics = () => {
      if (compareMetricsRef.current) return;

      getMetrics(pipelineVersion, selectedSamples).then((data) =>
        setMetrics(data)
      );
    };

    const intervalId = setInterval(fetchMetrics, 5000);

    return () => clearInterval(intervalId);
  }, [pipelineVersion, selectedSamples]);

  const handleSampleChange = (sample) => {
    if (compareMetrics) setCompareMetrics(false);
    getMetrics(pipelineVersion, [...selectedSamples, sample]).then((data) =>
      setMetrics(data)
    );
    setSelectedSamples((prev) =>
      prev.includes(sample)
        ? prev.filter((s) => s !== sample)
        : [...prev, sample]
    );
  };

  const handleStartValidation = () => {
    const requestBody = {
      sampleNames: selectedSamples,
      version: pipelineVersion,
    };

    const checkValidationStatus_ = (promiseId) => {
      setTimeout(() => {
        checkValidationStatus(promiseId).then((data) => {
          if (data["status"] == "PROGRESS") {
            console.log("Metrics are calculating");
            checkValidationStatus_(promiseId);
          } else if (data["status"] == "FAILURE") {
            enqueueSnackbar(
              `Error while calculating metrics: ${data["details"]}`,
              {
                variant: "error",
              }
            );
          } else {
            enqueueSnackbar("Metrics calculation completed", {
              variant: "success",
            });
          }
        });
      }, 5000);
    };

    startValidation(requestBody).then((promiseId) => {
      checkValidationStatus_(promiseId);
    });
  };

  const handleCompareMetrics = () => {
    setCompareMetrics(true);
    const requestBody = {
      sampleNames: selectedSamples,
      currentVersion: pipelineVersion,
      comparedVersion: pipelineVersionToCompare,
    };

    compareMetricsAPI(requestBody).then((data) => setMetrics(data));
  };

  const handleSetPipelineVersion = (pipelineVersionValue) => {
    setPipelineVersion(pipelineVersionValue);
    getMetrics(pipelineVersionValue, selectedSamples).then((data) =>
      setMetrics(data)
    );
  };

  const handleAddSampleDialogClose = () => {
    setOpenDialog(false);
    getSamples().then((data) => setSamples(data));
  };

  return (
    <ThemeProviderWrapper>
      <Box
        p={4}
        display="flex"
        flexDirection="column"
        justifyContent="space-between"
        gap={4}
      >
        <Typography variant="h3" textAlign="center">
          BioValidator
        </Typography>

        <Box display="flex" flexGrow={1} gap={4} height="75vh">
          <Stack direction="column" flex="1" spacing={3}>
            <Typography variant="h4" textAlign="center">
              Samples for validation
            </Typography>

            <Button
              variant="contained"
              color="primary"
              onClick={() => setOpenDialog(true)}
            >
              Add new sample
            </Button>

            <SampleList
              samples={samples}
              selectedSamples={selectedSamples}
              handleSampleChange={handleSampleChange}
            />

            <PipelinesVersionSelector
              value={pipelineVersion}
              onChange={handleSetPipelineVersion}
              pipelineVersions={["1", "2", "3"]}
              label="Pipeline version"
            />

            <Button
              variant="contained"
              color="primary"
              sx={{ height: 50 }}
              fullWidth
              onClick={handleStartValidation}
            >
              Start validation
            </Button>
          </Stack>

          <Stack direction="column" flex="2" spacing={3}>
            <Typography variant="h4" textAlign="center">
              Metrics
            </Typography>

            <TableContainer
              overflow="auto"
              sx={{
                border: "1px solid #e0e0e0",
                borderRadius: "8px",
                height: "calc(90vh - 250px)",
              }}
            >
              {compareMetrics ? (
                <CompareMetricsTable metrics={metrics} />
              ) : (
                <MetricsTable metrics={metrics} />
              )}
            </TableContainer>

            <ComparePipelineVersion
              pipelineVersionToCompare={pipelineVersionToCompare}
              pipelineVersions={["1", "2", "3"]}
              setPipelineVersionToCompare={setPipelineVersionToCompare}
              handleCompareMetrics={handleCompareMetrics}
            />
          </Stack>
        </Box>
      </Box>

      <AddSampleDialog
        open={openDialog}
        onClose={handleAddSampleDialogClose}
        setSamples={setSamples}
        samples={samples}
      />
    </ThemeProviderWrapper>
  );
};

export default App;
