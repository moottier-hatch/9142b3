import React from "react";

import { Badge, Box } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  root: {
    display: "flex",
    justifyContent: "space-between",
    marginRight: 20,
    flexGrow: 1,
  },
}));

const UnreadNotification = ({ conversation, nUnread }) => {
  const classes = useStyles();
  return (
    <Box className={classes.root}>
      <Badge badgeContent={nUnread} color="primary"></Badge>
    </Box>
  );
};
  
  export default UnreadNotification;