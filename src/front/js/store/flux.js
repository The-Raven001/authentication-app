const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      token: null,
      demo: [
        {
          title: "FIRST",
          background: "white",
          initial: "white",
        },
        {
          title: "SECOND",
          background: "white",
          initial: "white",
        },
      ],
    },
    actions: {
      register: async (email, password) => {
        try {
          const response = await fetch(
            process.env.BACKEND_URL + "/api/signup",
            {
              method: "POST",
              headers: {
                "Content-type": "application/json",
              },
              body: JSON.stringify({ email, password }),
            }
          );
          if (!response.ok) {
            return false;
          }
          const data = await response.json();
          return data;
        } catch (error) {
          console.log(error);
        }
      },
      login: async (email, password) => {
        try {
          const response = await fetch(process.env.BACKEND_URL + "/api/login", {
            method: "POST",
            headers: {
              "Content-type": "application/json",
            },
            body: JSON.stringify({ email, password }),
          });
          if (!response.ok) {
            console.log("Response not OK:", response);
            return false;
          }
          const data = await response.json();
          console.log("Login response data:", data);
          localStorage.setItem("token", data.token);
          setStore({ token: data.token });
          return true;
        } catch (error) {
          console.log("Login error:", error);
        }
      },

      validateToken: async () => {
        const token = localStorage.getItem("token");

        if (!token) {
          return;
        }

        try {
          const response = await fetch(
            `${process.env.BACKEND_URL}/api/private`,
            {
              method: "GET",
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

          if (response.ok) {
            setStore({ token: token });
            return true;
          } else {
            localStorage.removeItem("token");
            return;
          }
        } catch (error) {
          console.error("Error validating token:", error);
          localStorage.removeItem("token");
          return;
        }
      },
    },
  };
};

export default getState;
