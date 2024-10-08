import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";
import "../../styles/home.css";

export const Home = () => {
  const { store, actions } = useContext(Context);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmitRegister = async (e) => {
    e.preventDefault();
    console.log(email, password);
    const response = await actions.register(email, password);
    console.log(response);
  };
  return (
    <div className="container d-flex justify-content-center mt-5">
      <form className="w-50" onSubmit={handleSubmitRegister}>
        <div className="mb-3">
          <h2 className="text-center">Register</h2>
          <label htmlFor="exampleInputEmail1" className="form-label">
            Email address
          </label>
          <input
            type="email"
            className="form-control"
            value={email}
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
            onChange={(e) => setEmail(e.target.value)}
          ></input>
          <div id="emailHelp" className="form-text">
            We'll never share your email with anyone else.
          </div>
        </div>
        <div className="mb-3">
          <label htmlFor="exampleInputPassword1" className="form-label">
            Password
          </label>
          <input
            type="password"
            value={password}
            className="form-control"
            onChange={(e) => setPassword(e.target.value)}
            id="exampleInputPassword1"
          ></input>
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
        <hr></hr>
        <div className="my-4">
          <Link to="/login">
            Posees una cuenta?
            <span className="text-primary"> Haz click aqui!</span>
          </Link>
        </div>
      </form>
    </div>
  );
};
