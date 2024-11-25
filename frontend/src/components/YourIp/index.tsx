import { FC, useEffect, useState } from "react";

const YourIp: FC = () => {
  const [localIp, setLocalIp] = useState<string>("");
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    fetch("https://api-bdc.net/data/client-ip/")
      .then((response) => {
        if (!response.ok) return;
        return response.json();
      })
      .then((data) => {
        setFetching(false);
        setLocalIp(data.ipString);
      })
      .catch((err) => console.error(err));
  }, []);

  if (!fetching)
    return (
      <div className="text-md font-semibold">
        Ваш IP &nbsp;
        <code
          className="bg-slate-500/20 p-0.5 mx-0.5 rounded cursor-pointer hover:bg-slate-500/30"
          onClick={() => navigator.clipboard.writeText(localIp)}
        >
          {localIp}
        </code>
      </div>
    );
};
export default YourIp;
