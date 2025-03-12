import React, { useContext, useEffect, useRef, useState } from "react";
import { Heading, Flex, Separator, Container, Box, Button, HStack, Input } from "@chakra-ui/react";
import { io } from "socket.io-client";
import { AuthContext } from "../App";

import Cookies from "js-cookie";

function Chat(props) {
  const { curChat } = props;
  const { curUser, setCurUser } = useContext(AuthContext)
  const [messages, setMessages] = useState([]);
  const socket = io("http://localhost:4000/", {
    autoConnect: true
  })
  const msgRef = useRef("");

  function sendMessage() {
    let text = msgRef.current.value;

    socket.send({ "chatId": curChat, "access_token": curUser, "text": text }, (res) => {
      setMessages(previous => [...previous, res])
    })
  }


  useEffect(() => {
    function onConnect() {
      socket.connect()
    }

    function onDisconnect() {
      socket.disconnect()
    }

    function update_messages(data) {
      setMessages(data)
    }
    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on("fetch_messages", (res) => {
      console.log(`fetched: ${res.data}`)
      update_messages(res.data);
    })
    socket.emit("fetch_messages", { "chatId": curChat })
    console.log("OK")
  }, [curChat])


  if (curChat == "") {
    return (
      <Container>
        <Box
          p="4"
          borderWidth="1px"
          borderColor="border.disabled"
          color="fg.disabled"
        >
          Somewhat disabled box
        </Box>
      </Container>
    )
  }


  console.log(messages)


  return (
    <Container>
      <Box
        p="4"
        borderWidth="1px"
        borderColor="border.disabled"
        color="fg.disabled"
      >
        {messages.map((msg) => (
          <Box
            p="4"
            borderWidth="1px"
            borderColor="border.disabled"
            color="fg.disabled"
          >{msg.text}</Box>
        ))}
      </Box>
      <HStack>
        <Input ref={msgRef} placeholder="Message" variant="outline" />
        <Button variant="outline" onClick={sendMessage}>Send</Button>
      </HStack>
    </Container>
  );
};

export default Chat;
