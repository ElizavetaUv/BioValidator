import React from "react";
import { Button } from "@mui/material";
import PipelinesVersionSelector from "./PipelinesVersionSelector";

const ComparePipelineVersion = ({
  pipelineVersionToCompare,
  pipelineVersions,
  setPipelineVersionToCompare,
  handleCompareMetrics,
}) => (
  <>
    <PipelinesVersionSelector
      value={pipelineVersionToCompare}
      onChange={setPipelineVersionToCompare}
      pipelineVersions={pipelineVersions}
      label="Pipeline version to compare"
    />
    <Button
      variant="contained"
      color="primary"
      sx={{ height: 50, fontSize: "1.2rem" }}
      fullWidth
      onClick={handleCompareMetrics}
    >
      Compare
    </Button>
  </>
);

export default ComparePipelineVersion;
