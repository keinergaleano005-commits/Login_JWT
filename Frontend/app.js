const API = "http://localhost:8000";

const formLogin = document.getElementById("form-login");
const panel = document.getElementById("panel");
const saludo = document.getElementById("saludo");
const mensaje = document.getElementById("mensaje");
const email = document.getElementById("email");
const password = document.getElementById("password");

async function iniciarSesion(correo, contrasena) {
  const datos = new URLSearchParams();
  datos.append("username", correo);
  datos.append("password", contrasena);

  const respuesta = await fetch(`${API}/login`, {
    method: "POST",
    body: datos,
  });

  if (!respuesta.ok) {
    mensaje.textContent = "Correo o contraseña incorrectos";
    return;
  }

  const { access_token } = await respuesta.json();
  localStorage.setItem("token", access_token);
  mensaje.textContent = "";
  await mostrarPanel();
}

async function mostrarPanel() {
  const token = localStorage.getItem("token");
  if (!token) return;

  const respuesta = await fetch(`${API}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!respuesta.ok) {
    cerrarSesion();
    return;
  }

  const usuario = await respuesta.json();
  saludo.textContent = `Hola, usuario ${usuario.id}`;
  formLogin.hidden = true;
  panel.hidden = false;
}

function cerrarSesion() {
  localStorage.removeItem("token");
  panel.hidden = true;
  formLogin.hidden = false;
}

formLogin.addEventListener("submit", (evento) => {
  evento.preventDefault();
  iniciarSesion(email.value, password.value);
});

document.getElementById("btn-salir").addEventListener("click", cerrarSesion);

mostrarPanel();
