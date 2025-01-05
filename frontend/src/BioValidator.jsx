import React, { useState } from "react";
import {
  Box,
  Button,
  Checkbox,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";

const BioValidator = () => {
  const [selectedSamples, setSelectedSamples] = useState([]);
  const [pipelineVersion, setPipelineVersion] = useState("");
  const [pipelineVersionToCompare, setPipelineVersionToCompare] = useState("");

  const samples = Array.from({ length: 10 }, (_, i) => `Sample ${i + 1}`);
  const metrics = Array.from({ length: 10 }, (_, i) => `Metric ${i + 1}`);

  const handleSampleChange = (sample) => {
    setSelectedSamples((prev) =>
      prev.includes(sample)
        ? prev.filter((s) => s !== sample)
        : [...prev, sample]
    );
  };

  return (
    <Box p={4}>
      <Typography variant="h4" textAlign="center" mb={4}>
        BioValidator
      </Typography>
      <Box display="flex" gap={4}>
        {/* Samples for validation */}
        <Box flex={1} border={1} borderColor="grey.300" borderRadius={2} p={2}>
          <Typography variant="h6">Samples for validation</Typography>
          {samples.map((sample) => (
            <Box key={sample} display="flex" alignItems="center">
              <Checkbox
                checked={selectedSamples.includes(sample)}
                onChange={() => handleSampleChange(sample)}
              />
              <Typography>{sample}</Typography>
            </Box>
          ))}
        </Box>

        {/* Metrics */}
        <Box flex={1} border={1} borderColor="grey.300" borderRadius={2} p={2}>
          <Typography variant="h6">Metrics</Typography>
          {metrics.map((metric) => (
            <Box key={metric}>
              <Typography>{metric}</Typography>
            </Box>
          ))}
        </Box>
      </Box>

      {/* Controls */}
      <Box display="flex" gap={4} mt={4}>
        <FormControl fullWidth>
          <InputLabel>Pipeline version</InputLabel>
          <Select
            value={pipelineVersion}
            onChange={(e) => setPipelineVersion(e.target.value)}
          >
            <MenuItem value="v1.0">v1.0</MenuItem>
            <MenuItem value="v2.0">v2.0</MenuItem>
            <MenuItem value="v3.0">v3.0</MenuItem>
          </Select>
        </FormControl>

        <FormControl fullWidth>
          <InputLabel>Pipeline version to compare</InputLabel>
          <Select
            value={pipelineVersionToCompare}
            onChange={(e) => setPipelineVersionToCompare(e.target.value)}
          >
            <MenuItem value="v1.0">v1.0</MenuItem>
            <MenuItem value="v2.0">v2.0</MenuItem>
            <MenuItem value="v3.0">v3.0</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Buttons */}
      <Box display="flex" gap={4} mt={4}>
        <Button variant="contained" color="primary" fullWidth>
          Start validation
        </Button>
        <Button variant="contained" color="primary" fullWidth>
          Compare
        </Button>
      </Box>
    </Box>
  );
};

export default BioValidator;
