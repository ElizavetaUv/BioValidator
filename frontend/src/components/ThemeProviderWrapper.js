import React from "react";
import { ThemeProvider, createTheme } from "@mui/material";

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

const ThemeProviderWrapper = ({ children }) => {
  return <ThemeProvider theme={theme}>{children}</ThemeProvider>;
};

export default ThemeProviderWrapper;
