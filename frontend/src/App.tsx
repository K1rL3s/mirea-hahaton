// import { downloadPDF } from './libs/pdf'
import { Provider } from "react-redux";

import { store } from "./store";

import { MainPage, ScanPage } from "./pages/";
import { BrowserRouter, Route, Routes } from "react-router-dom";

const App = () => (
  <Provider store={store}>
    <BrowserRouter>
      <Routes>
        <Route path={"/"}>
          <Route index element={<MainPage />} />
          <Route path="scans/:scanId" element={<ScanPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </Provider>
);
{
  /* <button onClick={downloadPDF}>Download</button> */
}

export default App;
