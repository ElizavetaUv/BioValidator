import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

const MetricsTable = ({ metrics }) => {
  const groupMetricsBySample = (data) => {
    const grouped = data.reduce((acc, metric) => {
      const { sampleName, name, value } = metric;

      if (!acc[sampleName]) {
        acc[sampleName] = {
          sampleName,
          TP: 0,
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
          <TableCell>True Positive variants</TableCell>
          <TableCell>False Negative variants</TableCell>
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
            <TableCell>{row["fn-genes"] || 0}</TableCell>
            <TableCell>{row["fp-genes"] || 0}</TableCell>
            <TableCell>
              {parseFloat(row["precision-gene"]).toFixed(7) || "N/A"}
            </TableCell>
            <TableCell>
              {parseFloat(row["recall-gene"]).toFixed(7) || "N/A"}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default MetricsTable;
