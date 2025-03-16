import React, { useContext, useEffect, useRef, useState } from "react";
import { Heading, Flex, Separator, Container, Box, Button, HStack, Input } from "@chakra-ui/react";
import { io } from "socket.io-client";
import { AuthContext } from "../App";
import { socket } from "./Socket";

import Cookies from "js-cookie";


function Chat(props) {
  const { curChat } = props;
  const { curToken, setCurToken } = useContext(AuthContext)
  const [messages, setMessages] = useState([]);

  const msgRef = useRef("");
  const sendMessage = () => {
    let text = msgRef.current.value;

    console.log("Socket state:", {
      connected: socket.connected,
      disconnected: socket.disconnected,
      id: socket.id,
    });

    socket.send({ "chatId": curChat, "access_token": curToken, "text": text })
    msgRef.current.value = ""

  }

  useEffect(() => {
    if (curChat != "") {
      socket.connect()

      function onJoin() {
        socket.emit("join_room", { "chatId": curChat, "userToken": curToken })
      }

      function onDisconnect() {
        socket.disconnect()
      }

      function onMessage() {
        console.log("OnMessage event")
        setMessages(previous => [...previous, res])
      }

      function update_messages(data) {
        setMessages(data)
      }

      socket.on("connect", () => { console.log("Connected with id: ", socket.id) })
      socket.on("disconnect", () => { console.log("Disconnected") })
      socket.on("join_room", onJoin)
      socket.on("message", (res) => {
        setMessages(previous => [...previous, res])
      })
      socket.on("update_messages", (res) => {
        update_messages(res);
      })

      // socket.emit("join_room", { "chatId": curChat })
      // socket.emit("fetch_messages", { "chatId": curChat })

      return () => {
        console.log("UNMOUNT")
        socket.disconnect()
        console.log(socket.disconnected)
        socket.off("connect", () => { console.log("Connected with id: ", socket.id) })
        socket.off("disconnect", () => { console.log("Disconnected") })
        socket.off("join_room", onJoin)
        socket.off("message", (res) => {
          setMessages(previous => [...previous, res])
        })
        socket.off("update_messages", (res) => {
          update_messages(res);
        })

      }
    }
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
    <Flex
      flexDirection="column"
      height="100%"
    >
      <Box
        p="4"
        borderWidth="1px"
        borderColor="border.disabled"
        color="fg.disabled"
        display="flex"
        flexDirection="column"
        gap="3"
        overflow="scroll"
        maxHeight="100%"
      >
        {messages.map((msg) => (
          <Box
            p="4"
            maxWidth="450px"
            alignSelf={msg.amISender ? "flex-end" : "flex-start"}
            borderWidth="1px"
            borderColor="border.disabled"
            color="fg.disabled"
          >{msg.text}</Box>
        ))}
      </Box>
      <HStack position="relative">
        <Input ref={msgRef} placeholder="Message" variant="outline" />
        <Button variant="outline" onClick={sendMessage}>Send</Button>
      </HStack>
    </Flex >
  );
};

export default Chat;
