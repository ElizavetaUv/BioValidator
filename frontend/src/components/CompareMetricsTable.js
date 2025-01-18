import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

const CompareMetricsTable = ({ metrics }) => {
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
  );
};

export default CompareMetricsTable;
