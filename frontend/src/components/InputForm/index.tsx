import { type FC, useRef, useState } from "react";
import { Input } from "../";
import { useNavigate } from "react-router-dom";
import AdvancedSettingsModal from "../AdvancedSettingsModal";
import { useSelector } from "react-redux";
import { RootState } from "../../store";

interface GetScanFormFields extends HTMLFormControlsCollection {
  ip?: HTMLInputElement;
  "ip-start"?: HTMLInputElement;
  "ip-end"?: HTMLInputElement;
  "ip-mask"?: HTMLInputElement;
  "ip-byte"?: HTMLSelectElement;
  "ip-format": HTMLInputElement;
  ports: HTMLInputElement;
  "custom-ports"?: HTMLInputElement;
}

interface GetScanFormElements extends HTMLFormElement {
  readonly elements: GetScanFormFields;
}

const InputForm: FC = () => {
  const navigate = useNavigate();
  const scanId = useRef<string | null>(null);
  const [customPorts, setCustomPorts] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const advancedSettings = useSelector(
    (state: RootState) => state.advancedSettingsSlice.settings,
  );

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setCustomPorts(e.target.value === "custom");
  };

  const handleSubmit = async (e: React.FormEvent<GetScanFormElements>) => {
    e.preventDefault();

    const { elements } = e.currentTarget;
    const ipFormat = elements["ip-format"].value;
    const singleFieldIp = elements.ip?.value;
    const ipStart = elements["ip-start"]?.value;
    const ipEnd = elements["ip-end"]?.value;
    const ipMask = elements["ip-mask"]?.value;
    const ipByte = elements["ip-byte"]?.value.toString();

    let ip: string;

    switch (ipFormat) {
      case "single":
      case "multiple": {
        ip = singleFieldIp!;
        break;
      }
      case "range": {
        ip = ipStart + ":" + ipEnd;
        break;
      }
      case "cidr": {
        ip = ipMask + "/" + ipByte;
        break;
      }
      default: {
        ip = "stfu";
        break;
      }
    }

    const portType = elements.ports.value;
    const ports = elements["custom-ports"]?.value;

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL ?? ""}/scans/`,
        {
          method: "POST",
          body: JSON.stringify({
            ...advancedSettings,
            ip,
            top_range: portType === "custom" ? null : parseInt(portType),
            specific_range: portType === "custom" ? ports : null,
            port_range: portType === "custom" ? "-p" : null,
          }),
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      const taskId = (await response.json()).task_id;
      if (!taskId) {
        throw Error("task id is undefined");
      }

      navigate(`/scans/${taskId}`);

      scanId.current = taskId;
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col items-center justify-center rounded-md p-6 my-2 bg-white border max-w-lg mx-auto"
    >
      <div className="flex flex-col items-start flex-grow gap-4 w-full">
        <Input />
        <div className="flex flex-col items-start w-full">
          <label htmlFor="ports" className="font-semibold mb-2">
            Выберите порты
          </label>
          <select
            id="ports"
            name="ports"
            onChange={handleSelectChange}
            className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
          >
            <option value="10">Топ 10 портов</option>
            <option value="100">Топ 100 портов</option>
            <option value="1000">Топ 1000 портов</option>
            <option value="custom">Указать свои порты</option>
          </select>
          {customPorts && (
            <input
              id="custom-ports"
              name="custom-ports"
              placeholder="1-40"
              className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 mt-2 w-full"
              required
            />
          )}
        </div>
        <div className="flex flex-col items-start w-full">
          <label htmlFor="location" className="font-semibold mb-2">
            Выберите локацию
          </label>
          <select
            id="location"
            name="location"
            onChange={handleSelectChange}
            className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
          >
            <option value="Rtu Mirea">РТУ Мирэа</option>
            <option value="Localhost">Localhost</option>
          </select>
        </div>
        <button
          type="button"
          onClick={() => setIsModalOpen(true)}
          className="px-4 py-2 text-white bg-secondary hover:bg-secondary-dark font-medium rounded-md transition duration-150 ease-in-out w-full mb-4"
        >
          Расширенные настройки
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-white bg-primary hover:bg-primary-dark font-medium rounded-md transition duration-150 ease-in-out w-full"
        >
          Сканировать
        </button>
      </div>
      <AdvancedSettingsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </form>
  );
};

export default InputForm;
