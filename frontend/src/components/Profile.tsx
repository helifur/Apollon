import React, { useEffect, useState, createContext, useContext } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  Input,
  DialogBody,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
  Stack,
  Text,
  DialogActionTrigger,
  Heading,
  Avatar,
  VStack,
} from "@chakra-ui/react";






export default function Profile(props) {
  const { onclck, profile } = props;

  return (
    <Box
      p="4"
      borderBottomWidth="2px"
      borderColor="border.disabled"
      color="fg.disabled"
      _hover={{ bg: "gray.300" }}
      _active={{ bg: "gray.400" }}
      _focus={{ bg: "gray.500" }}
      _disabled={{ opacity: "0.5" }}
      key={profile.chatId}
      onClick={() => onclck(profile.chatId)}
    >
      <Flex>
        <Avatar.Root size="2xl">
          <Avatar.Fallback key={profile.username} name={profile.username} />
          <Avatar.Image src="https://bit.ly/sage-adebayo" />
        </Avatar.Root>
        <Box ml="4">
          <Heading size="xl">{profile.username}</Heading>
          <Text
            key={profile.chatId}
          >{profile.chatId}</Text>
        </Box>
      </Flex>
    </Box>
  )
}
