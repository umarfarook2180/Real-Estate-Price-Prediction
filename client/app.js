function getBathValue() {
  const uiBathrooms = document.getElementsByName("uiBathrooms");
  for (const bathroom of uiBathrooms) {
    if (bathroom.checked) {
        return parseInt(bathroom.value, 10);
    }
  }
  return -1;
}

function getBHKValue() {
  const uiBHK = document.getElementsByName("uiBHK");
  for (const bhk of uiBHK) {
    if (bhk.checked) {
        return parseInt(bhk.value, 10);
    }
  }
  return -1;
}

function getApiBaseUrl() {
  return window.location.protocol === "file:" ? "http://127.0.0.1:5000" : "";
}

function setResult(message, isError) {
  const estPrice = document.getElementById("uiEstimatedPrice");
  estPrice.textContent = message;
  estPrice.classList.toggle("error", Boolean(isError));
}

async function onClickedEstimatePrice() {
  const sqft = document.getElementById("uiSqft");
  const bhk = getBHKValue();
  const bathrooms = getBathValue();
  const location = document.getElementById("uiLocations");
  const totalSqft = parseFloat(sqft.value);

  if (!Number.isFinite(totalSqft) || totalSqft <= 0) {
    setResult("Enter a valid area", true);
    return;
  }

  if (!location.value) {
    setResult("Choose a location", true);
    return;
  }

  try {
    const response = await fetch(`${getApiBaseUrl()}/predict_home_price`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        total_sqft: totalSqft,
        bhk: bhk,
        bath: bathrooms,
        location: location.value
      })
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to estimate price");
    }

    setResult(`${data.estimated_price} Lakh`, false);
  } catch (error) {
    setResult(error.message, true);
  }
}

async function onPageLoad() {
  const uiLocations = document.getElementById("uiLocations");

  try {
    const response = await fetch(`${getApiBaseUrl()}/get_location_names`);
    const data = await response.json();

    uiLocations.replaceChildren(new Option("Choose a Location", ""));
    data.locations.forEach((location) => {
      uiLocations.append(new Option(location, location));
    });
  } catch (error) {
    setResult("Could not load locations", true);
  }
}

window.onload = onPageLoad;
