// issue #2: unread status
// MessageNotification component displays # of unread messages for a conversation
import React from "react";

import { Box } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  root: {
    display: "flex",
    justifyContent: "space-between",
    marginRight: 20,
    flexGrow: 1,
  },
  circle: {
    display: "flex",
    width: 20,
    height: 20,
    backgroundColor: "#3F92FF",
    borderRadius: "10px",
    alignItems: "center",
    justifyContent: "center",
  },
  count: {
    fontFamily: "Open Sans",
    fontSize: "10px",
    fontWeight: 700,
    lineHeight: "14px",
    letterSpacing: "-0.5px",
    textAlign: "left",   
    color: "#FFFFFF", 
    height: "14px",
    left: "89%",
    right: "9%",
    top: "calc(50% - 14px/2)",
  },
}));

const UnreadNotification = ({ conversation, nUnread }) => {
  const classes = useStyles();

  return (
    <Box className={classes.root}>
      <div className={classes.circle}>
        <span className={classes.count}>{nUnread}</span>
      </div>
    </Box>
  );
};
  
  export default UnreadNotification;