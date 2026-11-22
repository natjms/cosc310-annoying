const API_URL = "/api";

/**
 * @param {string} endpoint
 * @param {string} [method='GET']
 * @param {any} [body=null]
 * @returns {Promise<any>}
 */

export async function apiCall(endpoint, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
  const token = localStorage.getItem("token");

  if (token) {
    headers["x-token"] = token;
  }

  const options = { method, headers };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_URL}${endpoint}`, options);

  if (response.status == 401) {
    localStorage.removeItem("token");
    window.location.href = "/";
    throw new Error("you are not authorized");
  }

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "sorry something went wrong");
  }

  if (response.status == 201) {
    return null;
  }

  return response.json();
}
