import React, { useState } from "react";
import {
  Button,
  Form,
  Grid,
  Header,
  Message,
  Segment,
  Divider,
  Checkbox,
  Container
} from "semantic-ui-react";
import { userSignin } from "../../ApiFetchers/posters/Axios";
import { getCurrentUsers } from "../../ApiFetchers/getters/Axios";

const SignInForm = () => {
  const [authenticated, setAuthenticated] = useState(false);
  const [auth, setAuth] = useState({
    email: "",
    username: "",
    password: "",
    error: "",
    loading: false,
    redirecting: false
  });
  const handleChange = name => event => {
    //simply sets the states using input value as user types
    setAuth({ ...auth, [name]: event.target.value });
  };
  const handleSubmit = e => {
    e.preventDefault();
    let { email, username, password } = auth;
    userSignin(email, username, password);
  };
  return (
    <Container>
      <Grid.Row>
        <Grid.Row>
          <Divider horizontal>Welcome to Hindle's Wonderland</Divider>
        </Grid.Row>
        <Grid.Row style={{ height: "100px" }}></Grid.Row>
        <Grid centered columns={2}>
          <Grid.Column>
            <Header as="h2" textAlign="center">
              Login
            </Header>
            <Segment>
              <Form size="large">
                <Form.Input
                  fluid
                  icon="envelope"
                  iconPosition="left"
                  name="email"
                  onChange={handleChange("email")}
                  placeholder="Email address"
                  required
                />
                <Form.Input
                  fluid
                  icon="user"
                  iconPosition="left"
                  name="username"
                  onChange={handleChange("username")}
                  placeholder="Email address"
                  required
                />
                <Form.Input
                  fluid
                  icon="lock"
                  iconPosition="left"
                  name="password"
                  onChange={handleChange("password")}
                  placeholder="Password"
                  type="password"
                  required
                />
                <Button color="blue" fluid size="large" onClick={handleSubmit}>
                  Login
                </Button>
                <br />
                <Grid.Row>
                  <Checkbox
                    label={{ children: "Remember Me" }}
                    style={{ float: "right" }}
                  />
                </Grid.Row>
                <br />
              </Form>
            </Segment>
            <Message>
              Not registered yet? <a href="/signup">Sign Up</a>
            </Message>
            <Message>
              Forgot Password? <a href="/forgot_password">Let Us Know</a>
            </Message>
          </Grid.Column>
        </Grid>
      </Grid.Row>
    </Container>
  );
};

export default SignInForm;
