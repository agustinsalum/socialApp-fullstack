import React, { useState } from "react";
import axios from "axios";
import { Form, Button, Container, Row, Col, Alert } from "react-bootstrap";

export const Register = () => {
  const [username, setUsername] = useState(''); 
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(''); // Error handling status
  const [success, setSuccess] = useState(''); // Success message status

  // Form submission method
  const submit = async (e) => {
    e.preventDefault();

    // Simple validation on the frontend
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const user = {
      username: username,
      email: email,
      password: password,
    };

    try {
      const { data } = await axios.post(
        "http://localhost:8000/api/register/",
        user,
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true, // If necessary
        }
      );

      setSuccess("Successful registration. You can log in now.");
      setError('');
      // Optional: Redirect to login automatically
      // window.location.href = "/login";
    } catch (err) {
      if (err.response && err.response.data) {
        // Handle validation errors
        const errorMessages = Object.values(err.response.data).flat();
        setError(errorMessages.join(" "));
      } else {
        setError("Connection error");
      }
      setSuccess('');
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md="6">
          <div className="Auth-form-container">
            <form className="Auth-form" onSubmit={submit}>
              <div className="Auth-form-content">
                <h3 className="Auth-form-title">Registro</h3>
                {error && <Alert variant="danger">{error}</Alert>}
                {success && <Alert variant="success">{success}</Alert>}
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

                <Form.Group controlId="formEmail" className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder="Enter Email"
                    value={email}
                    required
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </Form.Group>

                <Form.Group controlId="formPassword" className="mb-3">
                  <Form.Label>Contraseña</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    required
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </Form.Group>

                <Form.Group controlId="formConfirmPassword" className="mb-3">
                  <Form.Label>Confirmar Contraseña</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Confirm password"
                    value={confirmPassword}
                    required
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </Form.Group>

                <Button variant="primary" type="submit" className="w-100">
                  Sign up
                </Button>
              </div>
            </form>
          </div>
        </Col>
      </Row>
    </Container>
  );
};
