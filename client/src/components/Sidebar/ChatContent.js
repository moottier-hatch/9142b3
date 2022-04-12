import React from "react";
import { Box, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { MessageNotification } from '../Sidebar/';

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    justifyContent: "space-between",
    marginLeft: 20,
    flexGrow: 1,
  },
  username: {
    fontWeight: "bold",
    letterSpacing: -0.2,
  },
  previewText: {
    fontSize: 12,
    color: "#9CADC8",
    letterSpacing: -0.17,
  },
  notificationWrap: {
    display: "flex",
    alignItems: "center",
  },
}));

const ChatContent = ({ conversation }) => {
  const classes = useStyles();

  const { otherUser } = conversation;
  const latestMessageText = conversation.id && conversation.latestMessageText;
  const nUnread = conversation.messages.filter((msg) => !msg.isRead && msg.senderId === otherUser.id).length;

  return (
    <Box className={classes.root}>
      <Box>
        <Typography className={classes.username}>
          {otherUser.username}
        </Typography>
        <Typography className={classes.previewText}>
          {latestMessageText}
        </Typography>
      </Box>
        {
          nUnread > 0 &&
          <Box className={classes.notificationWrap}>
            <MessageNotification conversation={conversation} nUnread={nUnread} />
          </Box>
        }
    </Box>
  );
};

export default ChatContent;
