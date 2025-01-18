import React from "react";
import { Box, Checkbox, Typography } from "@mui/material";

const SampleList = ({ samples, selectedSamples, handleSampleChange }) => (
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
);

export default SampleList;
