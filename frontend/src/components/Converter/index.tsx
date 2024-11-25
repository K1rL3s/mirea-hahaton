import { ChangeEvent, FC, useCallback, useState } from "react";
import { motion } from "motion/react";

import { inView } from "../../utils";
import { opacityVariant } from "../../utils/animation";

// interface IState {
// 	ip: string
// 	domen: string
// }

interface IData {
  ip_or_domain: string[];
}

const Converter: FC = () => {
  const [value, setValue] = useState<string>("");
  const [result, setResult] = useState<IData | null>({
    ip_or_domain: [],
  });

  const changeHandler = (e: ChangeEvent<HTMLInputElement>): void => {
    setValue(e.target.value);
  };

  const submitHandler = useCallback(() => {
    fetch(
      `${
        import.meta.env.VITE_API_BASE_URL ?? ""
      }/convert/?ip_or_domain=${value}/`,
    )
      .then((response) => {
        if (!response.ok) return;
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setResult(data);
      });
  }, [value]);

  return (
    <div className="grid sm:grid-cols-2 gap-5 sm:gap-16 w-full">
      <div className="flex flex-col gap-2 items-start sm:items-stretch">
        <span className="text-sm font-semibold">Домен</span>
        <input
          onChange={changeHandler}
          value={value}
          required
          placeholder="google.com"
          className="block border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary rounded-md px-3 py-2"
        />
        <button
          onClick={submitHandler}
          className="w-[250px] sm:w-auto px-4 py-2 text-primary hover:text-white border border-primary hover:bg-primary font-medium rounded-md transition duration-150 ease-in-out"
        >
          Конвертировать
        </button>
      </div>
      <div className="flex flex-col gap-2 items-stretch">
        <span className="text-sm font-semibold">IP адреса и домены</span>
        <ul className="flex flex-col pl-5 list-disc gap-1">
          {result?.ip_or_domain.map((ip, index) => (
            <motion.li key={index} {...inView} variants={opacityVariant()}>
              {ip}
            </motion.li>
          ))}
        </ul>
      </div>
    </div>
  );
};
export default Converter;
