import React, { useState, useEffect, useContext } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

const ProtectedRoute = ({ children }) => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  useEffect(() => {
    validateToken();
  }, [store.token]);

  async function validateToken() {
    const isValidToken = await actions.validateToken();
    if (!isValidToken) {
      navigate("/login");
    }
  }

  return children;
};

export default ProtectedRoute;
