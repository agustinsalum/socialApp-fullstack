
import React, { useState } from "react";
import axios from "axios";
import { Form, Button, Container, Row, Col, Alert } from "react-bootstrap";

export const Login = () => {
  const [username, setUsername] = useState(''); 
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // State to handle errors

  // Form submission method
  const submit = async (e) => {
    e.preventDefault();
    const user = {
      username: username,
      password: password,
    };

    try {
      // Create the POST request
      const { data } = await axios.post(
        "http://localhost:8000/api/token/",
        user,
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true, // Ensure that cookies are sent if necessary
        }
      );

      // Initialize the tokens in localStorage
      localStorage.clear();
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);

      // Set the authorization token for future requests
      axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

      // Redirect the user to the homepage
      window.location.href = "/";
    } catch (err) {
      // Handle authentication errors
      if (err.response && err.response.data) {
        setError(err.response.data.detail || "Authentication error");
      } else {
        setError("Connection error");
      }
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md="6">
          <div className="Auth-form-container">
            <form className="Auth-form" onSubmit={submit}>
              <div className="Auth-form-content">
                <h3 className="Auth-form-title">Sign In</h3>
                {error && <Alert variant="danger">{error}</Alert>}
                <Form.Group controlId="formUsername" className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter Username"
                    value={username}
                    required
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </Form.Group>

                <Form.Group controlId="formPassword" className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    required
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </Form.Group>

                <Button variant="primary" type="submit" className="w-100">
                  Submit
                </Button>
              </div>
            </form>
          </div>
        </Col>
      </Row>
    </Container>
  );
};
