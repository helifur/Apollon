import React, { createContext, createRef, useRef, useState, useContext } from "react";
import { Avatar, For, HStack, Button } from "@chakra-ui/react"
import { AuthContext } from "../App";


export default function MiniProfile() {
  const { curUser, setCurUser } = useContext(AuthContext);

  function handleLogout() {
    document.cookie = "access_token=; Max-Age=-1;";
    setCurUser("");
  }

  return (
    <HStack gap="3">
      <Avatar.Root size="xs" key="xs">
        <Avatar.Fallback name="Segun Adebayo" />
        <Avatar.Image src="https://bit.ly/sage-adebayo" />
      </Avatar.Root>
      <Button size="xs" colorPalette="red" variant="outline" onClick={handleLogout}>Logout</Button>
    </HStack>
  )
}
