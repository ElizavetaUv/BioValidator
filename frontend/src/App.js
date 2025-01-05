import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Checkbox,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
  Stack,
  createTheme,
  ThemeProvider,
} from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#4B61EC",
    },
  },
  typography: {
    allVariants: {
      color: "#060D3A",
    },
  },
});

const API_PATH = "http://localhost:8083";

const App = () => {
  const [samples, setSamples] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const pipelineVersions = ["1.0", "2.0", "3.0"];

  const [selectedSamples, setSelectedSamples] = useState([]);
  const [pipelineVersion, setPipelineVersion] = useState("");
  const [pipelineVersionToCompare, setPipelineVersionToCompare] = useState("");

  useEffect(() => {
    fetch(`${API_PATH}/samples`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Samples:", data);
        setSamples(data);
      })
      .catch((error) => console.error("Error fetching samples:", error));
  }, []);

  const samplesDump = Array.from({ length: 50 }, (_, i) => `Sample ${i + 1}`);
  const metricsDump = Array.from({ length: 50 }, (_, i) => `Metric ${i + 1}`);
  const metricsDumpData = [
    { name: "TP", version: "1.0", value: "4", sample_id: "NA127" },
    { name: "TF", version: "1.0", value: "32", sample_id: "NA127" },
    { name: "FN", version: "1.0", value: "67", sample_id: "NA127" },
    { name: "TP", version: "1.0", value: "3", sample_id: "NA127" },
    { name: "FN", version: "1.0", value: "87", sample_id: "NA127" },
    { name: "TP", version: "1.0", value: "9", sample_id: "NA127" },
    { name: "FN", version: "1.0", value: "35", sample_id: "NA127" },

    {},
  ];

  const handleSampleChange = (sample) => {
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

    fetch(`${API_PATH}/metrics/calculate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => {
        if (response.ok) {
          alert("Validation started successfully!");
        } else {
          throw new Error("Validation failed");
        }
      })
      .catch((error) => alert(`Error starting validation: ${error.message}`));
  };

  const handleCompareMetrics = () => {
    const requestBody = {
      sampleNames: selectedSamples,
      currentVersion: pipelineVersion,
      comparedVersion: pipelineVersionToCompare,
    };

    fetch(`${API_PATH}/metrics/compare`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Comparison result:", data);
        setMetrics(data);
      })
      .catch((error) => alert(`Error comparing metrics: ${error.message}`));
  };

  return (
    <ThemeProvider theme={theme}>
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

            <Box
              border={1}
              borderColor="grey.300"
              borderRadius={2}
              p={2}
              overflow="auto"
              sx={{ maxHeight: "calc(90vh - 250px)" }}
            >
              {samplesDump.map((sample) => (
                <Box
                  key={sample}
                  display="flex"
                  alignItems="center"
                  sx={{ height: 50 }}
                >
                  <Checkbox
                    checked={selectedSamples.includes(sample)}
                    onChange={() => handleSampleChange(sample)}
                  />
                  <Typography variant="h6">{sample}</Typography>
                </Box>
              ))}
            </Box>

            <FormControl fullWidth>
              <InputLabel id="PipelineVersion" sx={{ fontSize: "1.2rem" }}>
                Pipeline version
              </InputLabel>
              <Select
                value={pipelineVersion}
                onChange={(e) => setPipelineVersion(e.target.value)}
                sx={{ height: 50, fontSize: "1.2rem" }}
                labelId="PipelineVersion"
                label="Pipeline version"
              >
                {pipelineVersions.map((pipelineVersion) => (
                  <MenuItem
                    key={pipelineVersion}
                    value={pipelineVersion}
                    sx={{ fontSize: "1.2rem" }}
                  >
                    {pipelineVersion}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Button
              variant="contained"
              color="primary"
              sx={{ height: 50, fontSize: "1.2rem" }}
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

            <Box
              border={1}
              borderColor="grey.300"
              borderRadius={2}
              p={2}
              overflow="auto"
              sx={{ maxHeight: "calc(90vh - 250px)" }}
            >
              {metricsDump.map((metric) => (
                <Box
                  key={metric}
                  display="flex"
                  alignItems="center"
                  sx={{ height: 50 }}
                >
                  <Typography variant="h6">{metric}</Typography>
                </Box>
              ))}
            </Box>

            <FormControl fullWidth>
              <InputLabel
                id="PipelineVersionCompare"
                sx={{ fontSize: "1.2rem" }}
              >
                Pipeline version to compare
              </InputLabel>
              <Select
                value={pipelineVersionToCompare}
                onChange={(e) => setPipelineVersionToCompare(e.target.value)}
                sx={{ height: 50, fontSize: "1.2rem" }}
                labelId="PipelineVersionCompare"
                label="Pipeline version to compare"
              >
                {pipelineVersions.map((pipelineVersion) => (
                  <MenuItem
                    key={pipelineVersion}
                    value={pipelineVersion}
                    sx={{ fontSize: "1.2rem" }}
                  >
                    {pipelineVersion}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Button
              variant="contained"
              color="primary"
              sx={{ height: 50, fontSize: "1.2rem" }}
              fullWidth
              onClick={handleCompareMetrics}
            >
              Compare
            </Button>
          </Stack>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;
