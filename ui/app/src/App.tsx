import React from "react";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import * as Bokeh from "bokehjs";

import { makeStyles, Theme } from "@material-ui/core/styles";
import { JsonItem } from "bokehjs/build/js/types/embed";

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

const getPlot = (): JSX.Element => {
  axios
    .get("http://localhost:4013/visual")
    .then((response: any) => {
      console.log(response);
      return JSON.parse(response.data);
    })
    .then((data: JsonItem) => {
      Bokeh.embed.embed_item(data, "bt_plot");
    });
  return <div>test</div>;
  // const res_json = JSON.parse(response);
  //   return <div>aa</div>;
};

// const apiClient = axios.create({
//     baseURL: 'localhost:4013',
//     responseType: 'json',
//     headers: {
//       'Content-Type': 'application/json'
//     }
//   });

export default function SimpleSelect() {
  const classes = useStyles();
  return (
    <Grid container className={classes.container}>
      <Grid item className={classes.item} xs={12}>
        <Paper className={classes.paper} square>
          <React.Fragment>
            {getPlot()}
            <div id="bt_plot"></div>
          </React.Fragment>

          {/* <div id="bt_plot"></div>
ddd
          <script>
            {fetch("http://localhost:4013/visual")
              .then(function(response) {
                return JSON.parse(response.text)
              })
              .then(function(item) {
                Bokeh.embed.embed_item(item);
              })}
            ;
          </script> */}
        </Paper>
      </Grid>
      <Grid item className={classes.item} xs={6}>
        <Paper className={classes.paper} square>
          Data
        </Paper>
      </Grid>
      <Grid item className={classes.item} xs={6}>
        <Paper className={classes.paper} square>
          Setting
        </Paper>
      </Grid>
    </Grid>
  );
}
