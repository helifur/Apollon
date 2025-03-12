import { useState, createContext, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { ChakraProvider, Flex, Container, Grid, GridItem } from '@chakra-ui/react'
import { defaultSystem } from "@chakra-ui/react"
import Header from "./components/Header";
import Profile from './components/Profile';
import Chat from "./components/Chat.tsx";
import { Menu } from "antd";



interface Companion {
  username: string
  chatId: string
}

export const AuthContext = createContext("");


function App() {
  const [curUser, setCurUser] = useState(false);
  const [curChat, setCurChat] = useState("");
  const [chat, setChat] = useState(-1);
  const ProfilesContext = createContext({
    profiles: [], fetchProfiles: () => { }
  });
  const [profiles, setProfiles] = useState([])
  const fetchProfiles = async () => {
    const response = await fetch("http://localhost:8000/chats", {
      credentials: "include", method: "GET"
    })
    const profiles = await response.json()

    if (profiles.data) {
      setProfiles(profiles.data)
    }

    else {
      setProfiles([])
    }
  }
  useEffect(() => {
    fetchProfiles()
  }, [curUser])


  function trigger(data) {
    console.log(data);
    setCurChat(data)
  }

  return (
    <ChakraProvider value={defaultSystem}>
      <AuthContext.Provider value={{ curUser, setCurUser }}>

        <Flex
          minWidth="100vh"
          minHeight="100vh"
          direction="column">
          <Header />

          <Flex flexGrow={1} p={2}>
            <Flex flexGrow={1} borderWidth="2px" direction="column" overflowY="auto" scrollbar="hidden">
              <ProfilesContext.Provider value={{ profiles, fetchProfiles }}>
                {profiles.map((profile: Companion) => (
                  <Profile onclck={trigger} profile={profile} />
                ))}

              </ProfilesContext.Provider>

            </Flex>

            <Chat curChat={curChat} />
          </Flex>
        </Flex>
      </AuthContext.Provider>
    </ChakraProvider>
  )
}

export default App
