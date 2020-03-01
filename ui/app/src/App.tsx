import React, { useState } from "react";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import * as Bokeh from "bokehjs";

import { makeStyles, Theme } from "@material-ui/core/styles";
import { JsonItem } from "bokehjs/build/js/types/embed";

import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";

import { ResultModel } from "./models/result";
import { Button } from "@material-ui/core";
import { async } from "q";

const useStyles = makeStyles((theme: Theme) => ({
  container: {
    flexGrow: 1,
    width: "100%",
    flexDirection: "row"
  },
  item: {
    padding: "5px",
    background: "red"
  },
  paper: {
    margin: "5px",
    elevation: 1,
    variant: "outlined"
  }
}));

const axios = require("axios").default;
// const getPlot = ():() => {
//     axios
//       .get("http://localhost:4013/visual")
//       .then((response: any) => {
//         return JSON.parse(response.data);
//       })
//       .then((data: JsonItem) => {
//         Bokeh.embed.embed_item(data, "bt_plot");
//       });
//   };

export default function BackTest() {
  const initial: ResultModel = {
    name: "",
    index: [""],
    data: []
  };
  const [summaryData, setSummaryData] = useState(initial);
  //   const [plotData, setPlotData] = useState();
  const getResult = async () => {
    try {
      let summaryRes = await axios.get("http://localhost:4013/run-test");
      let plotRes = await axios.get("http://localhost:4013/visual-test");
      let summary = JSON.parse(summaryRes.data);
      let plot = JSON.parse(plotRes.data);
      let el = document.getElementById("bt_plot");
      if (el) {
        el.textContent = "";
      }
      Bokeh.embed.embed_item(plot);
      setSummaryData(summary);
    } catch (error) {
      console.log(error);
    }
  };

  const classes = useStyles();
  return (
    <Grid container className={classes.container}>
      <Grid item className={classes.item} xs={12}>
        <Paper className={classes.paper} square>
          <div id="bt_plot"></div>
        </Paper>
      </Grid>
      <Grid item className={classes.item} xs={6}>
        {/* <Paper className={classes.paper} square> */}
        <TableContainer component={Paper}>
          <Table aria-label="simple table" size="small">
            <TableHead>
              {summaryData.index.map((item: any, index: any) => (
                <TableRow key={index}>
                  <TableCell align="right">{item}</TableCell>
                  <TableCell align="right">{summaryData.data[index]}</TableCell>
                </TableRow>
              ))}
            </TableHead>
            <TableBody></TableBody>
          </Table>
        </TableContainer>
        {/* </Paper> */}
      </Grid>
      <Grid item className={classes.item} xs={6}>
        <Paper className={classes.paper} square>
          Setting
        </Paper>
      </Grid>
      <Button
        variant="contained"
        style={{ margin: 10 }}
        color="primary"
        onClick={getResult}
      >
        get plot
      </Button>
    </Grid>
  );
}
