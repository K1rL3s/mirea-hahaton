import { FC, useCallback, useRef, useState } from "react";
import { multipleIpPattern } from "../../utils/regEx";

const Input: FC = () => {
  const input = useRef<HTMLInputElement | null>(null);
  const [ipFormat, setIpFormat] = useState<string>("single");

  return (
    <>
      <div className="mb-4 w-full">
        <label className="font-semibold mr-2 mb-2 flex justify-center">
          Выберите формат IP адреса
        </label>
        <div className="flex gap-4 justify-around">
          <label className="flex  items-center gap-2">
            <input
              type="radio"
              name="ip-format"
              value="single"
              checked={ipFormat === "single"}
              onChange={() => setIpFormat("single")}
            />
            Один IP
          </label>
          <label className="flex items-center gap-2">
            <input
              type="radio"
              name="ip-format"
              pattern={multipleIpPattern}
              value="multiple"
              checked={ipFormat === "multiple"}
              onChange={() => setIpFormat("multiple")}
            />
            Несколько IP
          </label>
          <label className="flex items-center gap-2">
            <input
              type="radio"
              name="ip-format"
              value="range"
              checked={ipFormat === "range"}
              onChange={() => setIpFormat("range")}
            />
            Диапазон
          </label>
          <label className="flex items-center gap-2">
            <input
              type="radio"
              name="ip-format"
              value="cidr"
              checked={ipFormat === "cidr"}
              onChange={() => setIpFormat("cidr")}
            />
            CIDR
          </label>
        </div>
      </div>

      <label htmlFor="ip-address" className="font-semibold mr-2">
        Введите IP адрес
      </label>
      {ipFormat === "single" && (
        <input
          type="text"
          id="ip-address"
          ref={input}
          placeholder="192.168.0.1"
          name="ip"
          className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
          required
        />
      )}
      {ipFormat === "multiple" && (
        <input
          id="ip-address"
          ref={input}
          placeholder="192.168.0.1 192.168.0.2"
          name="ip"
          className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
          required
        />
      )}
      {ipFormat === "range" && (
        <div className="flex gap-2 w-full">
          <input
            type="text"
            id="ip-range-start"
            ref={input}
            placeholder="192.168.0.0"
            name="ip-start"
            className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
            required
          />
          <span className="text-3xl font-light">-</span>
          <input
            type="text"
            placeholder="192.168.0.155"
            id="ip-range-end"
            name="ip-end"
            className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
            required
          />
        </div>
      )}
      {ipFormat === "cidr" && (
        <div className="flex gap-2 w-full">
          <input
            type="text"
            id="ip-cidr-mask"
            ref={input}
            placeholder="192.168.0.255"
            name="ip-mask"
            className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
            required
          />
          <span className="text-3xl font-light">/</span>
          <select
            id="ip-cidr-byte"
            name="ip-byte"
            className="border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2 w-full"
            required
          >
            {Array(33)
              .fill(0)
              .map((_: number, i) => i)
              .slice(25, 33)
              .map((v: number) => {
                return (
                  <option key={v} value={v.toString()}>
                    {v}
                  </option>
                );
              })}
          </select>
        </div>
      )}
    </>
  );
};

export default Input;
