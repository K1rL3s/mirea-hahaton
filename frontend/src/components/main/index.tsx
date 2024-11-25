import { FC } from "react";
import { motion } from "motion/react";

import SectionWrapper from "../../hocs/SectionWrapper";

import { InputForm, Converter } from "../";
import { fadeIn, inView } from "../../utils";
import { textVariant } from "../../utils/animation";

const mainPorts = [
  { id: 0, content: "21 File Transfer (FTP)" },
  { id: 1, content: "22 Secure Shell (SSH)" },
  { id: 2, content: "23 Telnet" },
  { id: 3, content: "25 Mail (SMTP)" },
  { id: 4, content: "80 Web (HTTP)" },
  { id: 5, content: "110 Mail (POP3)" },
  { id: 6, content: "143 Mail (IMAP)" },
  { id: 7, content: "443 SSL/TLS (HTTPS)" },
  { id: 8, content: "445 Microsoft (SMB)" },
  { id: 9, content: "3389 Remote (RDP)" },
];

const PortCard: FC<{ content: string }> = ({ content }) => {
  return (
    <div className="py-0.5 px-1.5 rounded-lg text-sm font-light bg-slate-500/30 cursor-pointer hover:bg-slate-500/40 transition-colors">
      {content}
    </div>
  );
};

const Main: FC = () => {
  return (
    <main className="overflow-hidden max-w-5xl mx-auto mt-8 px-4 flex flex-col items-center justify-start">
      <div className="text-secondary container w-full bg-white flex flex-col rounded-xl shadow p-4">
        <motion.h2
          {...inView}
          variants={textVariant(0.1)}
          className="text-2xl text-primary font-semibold mt-4"
        >
          Nmap Online Port Scanner
        </motion.h2>
        <hr className="my-4" />
        <div className="grid gap-8 grid-cols-1 md:grid-cols-2">
          <motion.p {...inView} variants={fadeIn("right", "spring", 0.2, 0.7)}>
            Выполните бесплатное сканирование портов, чтобы проверить любой
            IP-адрес и протестировать 10 общих TCP-портов с включенной версией
            обнаружения Nmap (-sV). Это быстрый и эффективный способ выявления
            уязвимостей в вашей сети.
          </motion.p>
          <motion.div {...inView} variants={fadeIn("left", "spring", 0.4, 0.7)}>
            <span className="text-span text-sm">Основные порты:</span>
            <div className="flex flex-wrap gap-2 mt-2">
              {mainPorts.map(({ id, content }) => (
                <PortCard key={id} content={content} />
              ))}
            </div>
          </motion.div>
        </div>
        <hr className=" my-4" />
        <motion.div {...inView} variants={fadeIn("right", "spring", 0.2, 1.5)}>
          <p className="text-md font-semibold sm:text-lg mb-4">
            Нужно конвертировать домен в IP или наоборот?
          </p>
          <Converter />
        </motion.div>

        <hr className="my-4" />
        <motion.div {...inView} variants={fadeIn("right", "spring", 0.4, 1.5)}>
          <InputForm />
        </motion.div>
      </div>
    </main>
  );
};

const MainSection = SectionWrapper(Main, "main");

export default MainSection;
