import React, { createContext, createRef, useRef, useState, useContext } from "react";
import { Heading, Flex, Stack, Button, Input, Badge, useDisclosure, Tabs } from "@chakra-ui/react";
import { Field } from "./ui/field";
import {
  DialogActionTrigger,
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";

import SignInDialog from "./SignInDialog";
import MiniProfile from "./MiniProfile";
import { AuthContext } from "../App";
import Cookies from "js-cookie";


export default function Header() {
  const { curToken, setCurToken } = useContext(AuthContext);


  if (curToken == false && document.cookie.indexOf("access_token") != -1) {
    setCurToken(Cookies.get("access_token"));
  }



  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="1rem"
      bg="gray.400"
      width="100%"
      top="0"
      left="0"
      right="0"
    >
      <Heading as="h1" size="sm">Test</Heading>
      {(curToken != "") ? <MiniProfile /> : <SignInDialog />}
    </Flex >
  );
};

