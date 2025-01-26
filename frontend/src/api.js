import { enqueueSnackbar } from "notistack";

const API_PATH = "http://localhost:8083";

export const getMetrics = (pipelineVersion, selectedSamples) => {
  const queryParams = new URLSearchParams();
  queryParams.append("version", pipelineVersion);
  selectedSamples.forEach((sampleName) => {
    queryParams.append("sampleName", sampleName);
  });

  return fetch(`${API_PATH}/metrics?${queryParams.toString()}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Metrics fetched:", data);
      return data;
    })
    .catch((error) => console.error("Error fetching metrics:", error));
};

export const getSamples = () => {
  return fetch(`${API_PATH}/samples`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Samples:", data);
      return data;
    })
    .catch((error) => console.error("Error fetching samples:", error));
};

export const compareMetricsAPI = (requestBody) => {
  return fetch(`${API_PATH}/metrics/compare`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Comparison result:", data);
      return data;
    })
    .catch((error) =>
      enqueueSnackbar(`Error comparing metrics: ${error.message}`, {
        variant: "error",
      })
    );
};

export const startValidation = (requestBody) => {
  return fetch(`${API_PATH}/metrics/calculate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  })
    .then((response) => {
      if (response.ok) {
        enqueueSnackbar("Validation started successfully!", {
          variant: "info",
        });
        return response.json();
      } else {
        throw new Error("Validation failed");
      }
    })
    .then((data) => data["promiseId"])
    .catch((error) =>
      enqueueSnackbar(`Error starting validation: ${error.message}`, {
        variant: "error",
      })
    );
};

export const checkValidationStatus = (promiseId) => {
  return fetch(`${API_PATH}/metrics/${promiseId}/calculate/status`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      return data;
    });
};
