import React from "react";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";

const PipelinesVersionSelector = ({
  value,
  onChange,
  pipelineVersions,
  label,
}) => (
  <FormControl fullWidth>
    <InputLabel sx={{ fontSize: "1.2rem" }}>{label}</InputLabel>
    <Select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      sx={{ height: 50, fontSize: "1.2rem" }}
      label={label}
    >
      {pipelineVersions.map((version) => (
        <MenuItem key={version} value={version} sx={{ fontSize: "1.2rem" }}>
          {version}
        </MenuItem>
      ))}
    </Select>
  </FormControl>
);

export default PipelinesVersionSelector;
