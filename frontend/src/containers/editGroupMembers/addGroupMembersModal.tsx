﻿import * as React from "react";
import { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import { Modal, Button, Form, Spinner } from "react-bootstrap";
import { Typeahead } from "react-bootstrap-typeahead";

import { MemberAdd, Student } from "../groupMembers/interfaces";
import { addMember, getStudents } from "./utils";
import { spinnerDivStyle, spinnerStyle } from "../clubsList/styles";

export function AddGroupMembersModal(props): JSX.Element {
  const { showModal, setShowModal, membersURL, setIsLoading, setMembers } =
    props;

  if (!showModal) {
    return <></>;
  }

  const [formData, setFormData] = useState<MemberAdd>({
    id: 0,
    function: "Membre",
    admin: false,
  });
  const [students, setStudents] = useState<Student[]>([]);
  const [isAddLoading, setIsAddLoading] = useState(false);

  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);

  const handleSubmit = (event: React.ChangeEvent<HTMLInputElement>) => {
    event.preventDefault();
    addMember(
      membersURL,
      formData,
      handleClose,
      setIsAddLoading,
      setIsLoading,
      setMembers
    );
  };

  useEffect(
    () => getStudents(props.studentsURL, setStudents, setIsAddLoading),
    []
  );

  if (isAddLoading) {
    return (
      <Modal
        show={showModal}
        onHide={handleClose}
        onSubmit={handleSubmit}
        key={students.length}
      >
        <Modal.Header closeButton>
          <Modal.Title>Ajout d'un.e membre</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <div className="grille" style={spinnerDivStyle}>
            <Spinner animation="border" role="status" style={spinnerStyle} />
          </div>
        </Modal.Body>
      </Modal>
    );
  }

  return (
    <Modal show={showModal} onHide={handleClose} onSubmit={handleSubmit}>
      <Modal.Header closeButton>
        <Modal.Title>Ajout d'un.e membre</Modal.Title>
      </Modal.Header>

      <Modal.Body style={isAddLoading ? { opacity: "0.4" } : null}>
        <Form>
          <Form.Group className="mb-3" controlId="formRole">
            <Form.Label>Etudiant.e</Form.Label>
            <Typeahead
              id="search-student"
              options={students.map((e) => {
                return { label: e.name, id: e.id };
              })}
              placeholder="Recherche"
              onChange={(student) => {
                if (typeof student[0] === "undefined") {
                  return;
                }
                let newFormData = formData;
                newFormData["id"] = student[0].id;
                setFormData(newFormData);
              }}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formRole">
            <Form.Label>Rôle</Form.Label>
            <Form.Control
              type="text"
              defaultValue={"Membre"}
              onChange={({ target: { value } }) => {
                let newFormData = formData;
                newFormData["role"] = value;
                setFormData(newFormData);
              }}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formDateBegin">
            <Form.Label>Date de début</Form.Label>
            <Form.Control
              type="date"
              onChange={({ target: { value } }) => {
                let newFormData = formData;
                newFormData["begin_date"] = value;
                setFormData(newFormData);
              }}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formDateEnd">
            <Form.Label>Date de fin</Form.Label>
            <Form.Control
              type="date"
              onChange={({ target: { value } }) => {
                let newFormData = formData;
                newFormData["end_date"] = value;
                setFormData(newFormData);
              }}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formAdmin">
            <Form.Check
              type="checkbox"
              label="Admin"
              defaultChecked={false}
              onChange={({ target: { value } }) => {
                let newFormData = formData;
                newFormData["admin"] = value === "on";
                setFormData(newFormData);
              }}
            />
          </Form.Group>
          <div style={{ float: "right" }}>
            <Button variant="primary" type="submit">
              Ajouter
            </Button>
          </div>
        </Form>
      </Modal.Body>
    </Modal>
  );
}
