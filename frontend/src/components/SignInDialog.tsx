import React, { createContext, createRef, useContext, useRef, useState } from "react";
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
import { AuthContext } from "../App";
import Cookies from "js-cookie";


export default function SignInDialog() {
  const nameRef = useRef(null);
  const usernameRef = useRef(null);
  const passwordRef = useRef(null);

  const usernameAuthRef = useRef(null);
  const passwordAuthRef = useRef(null);

  const [currentTab, setCurrentTab] = useState("register");
  const [loading, setLoading] = useState(false);

  const [invalidName, setInvalidName] = useState(false);
  const [invalidUsername, setInvalidUsername] = useState(false);
  const [invalidPassword, setInvalidPassword] = useState(false);
  const [invalidUsernameAuth, setInvalidUsernameAuth] = useState(false);
  const [invalidPasswordAuth, setInvalidPasswordAuth] = useState(false);

  const { curToken, setCurToken } = useContext(AuthContext);


  const handleTab = async (e) => {
    setCurrentTab(e.target.getAttribute("data-value"));
  }

  const handleReg = async () => {
    console.log(currentTab);

    if (currentTab == "register") {

      if (nameRef.current.value == "") {
        setInvalidName(true);
        return
      }
      if (usernameRef.current.value == "") {
        setInvalidUsername(true);
        return
      }
      if (passwordRef.current.value == "") {
        setInvalidPassword(true);
        return
      };
      setLoading(true);
      const response = await fetch(
        "http://localhost:8000/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: nameRef.current.value,
          username: usernameRef.current.value,
          password: passwordRef.current.value
        })
      });
    }

    else {
      if (usernameAuthRef.current.value == "") {
        setInvalidUsernameAuth(true);
        return
      }
      if (passwordAuthRef.current.value == "") {
        setInvalidPasswordAuth(true);
        return
      };
      setLoading(true);
      const request = await fetch(
        "http://localhost:8000/auth/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: usernameAuthRef.current.value,
          password: passwordAuthRef.current.value
        })
      });

      const response = request.json();
      const data = response.then((value) => {
        if (value.status == 200) {
          setCurToken(Cookies.get("access_token"));
          console.log(Cookies.get("access_token"));
        }
      });

    };
  }


  return (
    <DialogRoot>
      <DialogTrigger asChild>
        <Button variant="outline">Sign in</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Account</DialogTitle>
        </DialogHeader>
        <DialogBody pb="4">
          <Tabs.Root defaultValue="register">
            <Tabs.List>
              <Tabs.Trigger value="register" onClick={handleTab}>
                Register
              </Tabs.Trigger>
              <Tabs.Trigger value="signin" onClick={handleTab}>
                Sign in
              </Tabs.Trigger>
            </Tabs.List>
            <Tabs.Content value="register">
              <Stack gap="4">
                <Field invalid={invalidName} required label="First Name">
                  <Input ref={nameRef} placeholder="First Name" />
                </Field>
                <Field invalid={invalidUsername} required direction="row" label="Username">
                  <Input ref={usernameRef} key="UsernameInput" placeholder="Username" />
                  {/*<BadgeContext.Provider value={{ usernameStatus, fetchUsername }}>
                  <Badge colorPalette={(usernameStatus == true) ? "green" : "red"} >Enter username</Badge>
                </BadgeContext.Provider>*/}
                </Field>
                <Field invalid={invalidPassword} required label="Password">
                  <Input ref={passwordRef} placeholder="Password" type="password" />
                </Field>
              </Stack>

            </Tabs.Content>
            <Tabs.Content value="signin">
              <Stack gap="4">
                <Field invalid={invalidUsernameAuth} required label="Username">
                  <Input ref={usernameAuthRef} placeholder="Username" />
                </Field>
                <Field invalid={invalidPasswordAuth} required label="Password">
                  <Input ref={passwordAuthRef} placeholder="Password" type="password" />
                </Field>
              </Stack>
            </Tabs.Content>
          </Tabs.Root>
        </DialogBody>
        <DialogFooter>
          <DialogActionTrigger asChild>
            <Button variant="outline">Cancel</Button>
          </DialogActionTrigger>
          <Button variant="surface" loading={loading} onClick={handleReg}>Enter</Button>
        </DialogFooter>
      </DialogContent>
    </DialogRoot>
  )
}
