import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../store";
import PortList from "../PortList";
import {
  ScanData,
  setScanData,
  setScanStatus,
  Status,
} from "../../store/slices/scanSlice";
import { ipToNumber } from "../../utils/ipToNumber";
import { downloadPDF } from "../../libs/pdf.tsx";
import { BiLoader } from "react-icons/bi";
import { FaCheck, FaCircle } from "react-icons/fa6";
import classNames from "classnames";
import styles from "./index.module.scss";

const Indicator = ({ status }: { status: Status }) => {
  if (status === "idle" || status === "done")
    return (
      <div className="flex items-center justify-center mb-4">
        <svg
          className="w-6 h-6 me-2 text-green-500 dark:text-green-400 flex-shrink-0"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
        </svg>
        <span className="text-2xl">Завершено!</span>
      </div>
    );
  if (status === "loading")
    return (
      <div className="flex items-center justify-center mb-4">
        <div role="status">
          <svg
            aria-hidden="true"
            className="w-6 h-6 me-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
            viewBox="0 0 100 101"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="currentColor"
            />
            <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentFill"
            />
          </svg>
          <span className="sr-only">Loading...</span>
        </div>
        <span className="text-2xl">Сканируем IP...</span>
      </div>
    );
};

const ScanView = ({ id }: { id: string }) => {
  const dispatch = useDispatch();
  const scanState = useSelector((state: RootState) => state.scanSlice);
  const intervalId = useRef<number | null>(null);
  const [expandedIps, setExpandedIps] = useState<string[]>([]);

  useEffect(() => {
    const stopLoading = (status: Status) => {
      if (intervalId.current !== null) {
        clearInterval(intervalId.current);
      }
      intervalId.current = null;
      dispatch(setScanStatus(status));
    };

    const loadScan = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL ?? ""}/scans/${id}/`,
      );
      const scanData: ScanData = await response.json();

      dispatch(setScanData(scanData));

      if (scanData?.end) {
        stopLoading("done");
      }

      return scanData;
    };

    dispatch(setScanStatus("loading"));
    intervalId.current = setInterval(loadScan, 3000);
    loadScan();

    return () => {
      stopLoading("idle");
    };
  }, [dispatch, id]);

  const toggleExpand = (ip: string) => {
    setExpandedIps((prev) =>
      prev.includes(ip) ? prev.filter((item) => item !== ip) : [...prev, ip],
    );
  };

  return (
    <div className="p-4 w-full">
      <Indicator status={scanState.status} />
      {scanState.status === "done" && (
        <button onClick={() => downloadPDF(scanState.data)}>
          Download as PDF
        </button>
      )}
      {scanState.data?.ips
        .slice()
        .sort((a, b) => ipToNumber(a.ip) - ipToNumber(b.ip))
        .map((ipData) => (
          <div
            key={ipData.ip}
            className="mb-4 p-4 border rounded-md shadow-md hover:cursor-pointer bg-white"
            onClick={() => toggleExpand(ipData.ip)}
          >
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold mb-2">IP: {ipData.ip}</h2>
                {ipData.end ? (
                  <FaCheck className="mb-2" size={24} />
                ) : (
                  <BiLoader
                    className={classNames("mb-2", styles.spinner)}
                    size={24}
                  />
                )}
              </div>
              <div className="flex gap-2">
                <div className="flex justify-center items-center rounded-full w-9 h-9 p-2 border bg-emerald-500">
                  {ipData.ports.open.length}
                </div>
                <div className="flex justify-center items-center rounded-full w-9 h-9 p-2 border bg-rose-500">
                  {ipData.ports.closed.length}
                </div>
              </div>
            </div>
            <p className="mb-2">PTR: {ipData.ptr || "Неизвестен"}</p>
            {expandedIps.includes(ipData.ip) && (
              <div className="mb-2">
                <PortList
                  open={ipData.ports.open}
                  closed={ipData.ports.closed}
                />
              </div>
            )}
          </div>
        ))}
    </div>
  );
};

export default ScanView;
