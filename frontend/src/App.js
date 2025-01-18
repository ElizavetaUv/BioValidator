import React, { useState, useEffect, useRef } from "react";
import { Box, Button, Typography, Stack, TableContainer } from "@mui/material";
import ThemeProviderWrapper from "./components/ThemeProviderWrapper";
import MetricsTable from "./components/MetricsTable";
import CompareMetricsTable from "./components/CompareMetricsTable";
import SampleList from "./components/SampleList";
import PipelinesVersionSelector from "./components/PipelinesVersionSelector";
import ComparePipelineVersion from "./components/ComparePipelinesVersion";
import {
  getMetrics,
  getSamples,
  compareMetricsAPI,
  startValidation,
  checkValidationStatus,
} from "./api";

const App = () => {
  const [samples, setSamples] = useState([]);
  const [metrics, setMetrics] = useState([]);

  const [selectedSamples, setSelectedSamples] = useState([]);
  const [pipelineVersion, setPipelineVersion] = useState("");
  const [pipelineVersionToCompare, setPipelineVersionToCompare] = useState("");
  const [compareMetrics, setCompareMetrics] = useState(false);
  const [validationPromiseId, setValidationPromiseId] = useState(null);
  const compareMetricsRef = useRef(compareMetrics);

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

    const intervalId = setInterval(fetchMetrics, 1000);

    return () => clearInterval(intervalId);
  }, [pipelineVersion, selectedSamples]);

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

    const checkValidationStatus_ = (promiseId) => {
      setTimeout(() => {
        checkValidationStatus(promiseId).then((data) => {
          if (data["status"] == "PROGRESS") {
            console.log("Metrics are calculating");
            checkValidationStatus_(promiseId);
          } else if (data["status"] == "FAILURE") {
            alert(`Error while calculating metrics: ${data["details"]}`);
          } else {
            alert("Metrics calculation completed");
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

            <SampleList
              samples={samples}
              selectedSamples={selectedSamples}
              handleSampleChange={handleSampleChange}
            />

            <PipelinesVersionSelector
              value={pipelineVersion}
              onChange={setPipelineVersion}
              pipelineVersions={["1", "2", "3"]}
              label="Pipeline version"
            />

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
            {/* </Box> */}

            <ComparePipelineVersion
              pipelineVersionToCompare={pipelineVersionToCompare}
              pipelineVersions={["1", "2", "3"]}
              setPipelineVersionToCompare={setPipelineVersionToCompare}
              handleCompareMetrics={handleCompareMetrics}
            />
          </Stack>
        </Box>
      </Box>
    </ThemeProviderWrapper>
  );
};

export default App;
