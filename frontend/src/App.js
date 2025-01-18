import React, { useState, useEffect, useRef } from "react";
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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
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
  const pipelineVersions = ["1", "2", "3"];

  const [selectedSamples, setSelectedSamples] = useState([]);
  const [pipelineVersion, setPipelineVersion] = useState("");
  const [pipelineVersionToCompare, setPipelineVersionToCompare] = useState("");
  const [compareMetrics, setCompareMetrics] = useState(false);
  const compareMetricsRef = useRef(compareMetrics);

  useEffect(() => {
    compareMetricsRef.current = compareMetrics;
  }, [compareMetrics]);

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

  useEffect(() => {
    if (
      !pipelineVersion ||
      selectedSamples.length === 0 ||
      compareMetricsRef.current
    )
      return;

    const fetchMetrics = () => {
      if (compareMetricsRef.current) return;
      const queryParams = new URLSearchParams({
        version: pipelineVersion,
        sampleName: selectedSamples.join(","),
      });

      fetch(`${API_PATH}/metrics?${queryParams.toString()}`, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Metrics fetched:", data);
          setMetrics(data);
        })
        .catch((error) => console.error("Error fetching metrics:", error));
    };

    const intervalId = setInterval(fetchMetrics, 1000);

    return () => clearInterval(intervalId);
  }, [pipelineVersion, selectedSamples]);

  const samplesDump = Array.from({ length: 50 }, (_, i) => `Sample ${i + 1}`);
  const metricsDump = Array.from({ length: 50 }, (_, i) => `Metric ${i + 1}`);
  const metricsDumpData = [
    { name: "TP", version: "1.0", value: "4", sample_id: "NA127" },
    { name: "TF", version: "1.0", value: "32", sample_id: "NA127" },
    { name: "FN", version: "1.0", value: "67", sample_id: "NA147" },
    { name: "TP", version: "1.0", value: "3", sample_id: "NA127" },
    { name: "FN", version: "1.0", value: "67", sample_id: "NA176" },
    { name: "precision", version: "1.0", value: "87", sample_id: "NA127" },
    { name: "TP", version: "1.0", value: "9", sample_id: "NA154" },
    { name: "TP", version: "1.0", value: "9", sample_id: "NA154" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA138" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA4" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA54" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA7465" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA24" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA64" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA96" },
    { name: "recall", version: "1.0", value: "6", sample_id: "NA456" },
  ];

  const handleSampleChange = (sample) => {
    if (compareMetrics) setCompareMetrics(false);
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
    setCompareMetrics(true);
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

  const groupMetricsBySample = (data) => {
    const grouped = data.reduce((acc, metric) => {
      const { sampleName, name, value } = metric;

      if (!acc[sampleName]) {
        acc[sampleName] = {
          sampleName,
          TP: 0,
          TN: 0,
          FP: 0,
          FN: 0,
          precision: 0,
          recall: 0,
        };
      }
      acc[sampleName][name] = value;

      return acc;
    }, {});

    return Object.values(grouped);
  };

  const groupComparedMetricsBySample = (data) => {
    const grouped = data.reduce((acc, metric) => {
      const {
        sampleName,
        currentVersion,
        comparedVersion,
        name,
        currentValue,
        comparedValue,
        diffValue,
      } = metric;

      if (!acc[sampleName]) {
        acc[sampleName] = {
          sampleName,
          currentVersion,
          comparedVersion,
          "tp-genes": null,
          "tn-genes": null,
          "fp-genes": null,
          "precision-gene": null,
          "recall-gene": null,
        };
      }

      acc[sampleName][name] = {
        currentValue: parseFloat(currentValue) || 0,
        diffValue: parseFloat(diffValue) || 0,
      };

      return acc;
    }, {});

    return Object.values(grouped);
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
              sx={{ height: "calc(90vh - 250px)" }}
            >
              {samples.map((sample) => (
                <Box
                  key={sample.name}
                  display="flex"
                  alignItems="center"
                  sx={{ height: 50 }}
                >
                  <Checkbox
                    checked={selectedSamples.includes(sample.name)}
                    onChange={() => handleSampleChange(sample.name)}
                  />
                  <Typography variant="h6">{sample.name}</Typography>
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

            {/* <Box
              border={1}
              borderColor="grey.300"
              borderRadius={2}
              p={2}
              overflow="auto"
              sx={{ maxHeight: "calc(90vh - 250px)" }}
            > */}
            {/* {metricsDump.map((metric) => (
                <Box
                  key={metric}
                  display="flex"
                  alignItems="center"
                  sx={{ height: 50 }}
                >
                  <Typography variant="h6">{metric}</Typography>
                </Box>
              ))} */}
            <TableContainer
              overflow="auto"
              sx={{
                border: "1px solid #e0e0e0",
                borderRadius: "8px",
                height: "calc(90vh - 250px)",
              }}
            >
              {compareMetrics ? (
                <Table stickyHeader>
                  <TableHead>
                    <TableRow
                      sx={{
                        backgroundColor: "#ECECEC",
                        "& .MuiTableCell-root": {
                          color: "#000",
                          fontWeight: "bold",
                        },
                      }}
                    >
                      <TableCell>Sample name</TableCell>
                      <TableCell>Current version</TableCell>
                      <TableCell>Compare version</TableCell>
                      <TableCell>True Positive variants</TableCell>
                      <TableCell>True Negative variants</TableCell>
                      <TableCell>False Positive variants</TableCell>
                      <TableCell>Precision</TableCell>
                      <TableCell>Recall</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {groupComparedMetricsBySample(metrics).map((row, index) => (
                      <TableRow key={index}>
                        <TableCell>{row.sampleName}</TableCell>
                        <TableCell>{row.currentVersion}</TableCell>
                        <TableCell>{row.comparedVersion}</TableCell>
                        <TableCell>
                          {row["tp-genes"]?.currentValue || 0} (
                          {row["tp-genes"]?.diffValue || "unchanged"})
                        </TableCell>
                        <TableCell>
                          {row["tn-genes"]?.currentValue || 0} (
                          {row["tn-genes"]?.diffValue || "unchanged"})
                        </TableCell>
                        <TableCell>
                          {row["fp-genes"]?.currentValue || 0} (
                          {row["fp-genes"]?.diffValue || "unchanged"})
                        </TableCell>
                        <TableCell>
                          {row["precision-gene"]?.currentValue || "N/A"} (
                          {row["precision-gene"]?.diffValue || "unchanged"})
                        </TableCell>
                        <TableCell>
                          {row["recall-gene"]?.currentValue || "N/A"} (
                          {row["recall-gene"]?.diffValue || "unchanged"})
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <Table stickyHeader>
                  <TableHead>
                    <TableRow
                      sx={{
                        backgroundColor: "#ECECEC",
                        "& .MuiTableCell-root": {
                          color: "#000",
                          fontWeight: "bold",
                        },
                      }}
                    >
                      <TableCell>Sample name</TableCell>
                      <TableCell>True Positive variants</TableCell>
                      <TableCell>True Negative variants</TableCell>
                      <TableCell>False Positive variants</TableCell>
                      <TableCell>Precision</TableCell>
                      <TableCell>Recall</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {groupMetricsBySample(metrics).map((row, index) => (
                      <TableRow key={index}>
                        <TableCell>{row["sampleName"]}</TableCell>
                        <TableCell>{row["tp-genes"] || 0}</TableCell>
                        <TableCell>{row["tn-genes"] || 0}</TableCell>
                        <TableCell>{row["fp-genes"] || 0}</TableCell>
                        <TableCell>{row["precision-gene"] || "N/A"}</TableCell>
                        <TableCell>{row["recall-gene"] || "N/A"}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </TableContainer>
            {/* </Box> */}

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
