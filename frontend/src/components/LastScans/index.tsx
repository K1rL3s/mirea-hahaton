import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../store";
import { useEffect, useRef } from "react";
import { setLastScans } from "../../store/slices/globalSlice";
import { Link } from "react-router-dom";
import { TimeAgo } from "../TimeAgo";

const LastScans = () => {
  const dispatch = useDispatch();
  const lastScans = useSelector(
    (state: RootState) => state.globalSlice.lastScans,
  );

  const intervalId = useRef<number | null>(null);

  useEffect(() => {
    const fetchLastScans = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL ?? ""}/scans/last/`,
      );
      const lastScans = await response.json();
      dispatch(setLastScans(lastScans));
    };

    if (!lastScans.length) {
      fetchLastScans();
    }
    if (intervalId.current === null)
      intervalId.current = setInterval(fetchLastScans, 5000);
  }, []);

  return (
    <div className="absolute right-0 mt-2 w-96 bg-white border rounded shadow-lg py-2">
      <div className="flex justify-center my-2 text-lg">Последние сканы</div>
      <ul className="flex gap-2 flex-col">
        {lastScans.map((scan) => (
          <li key={`${scan?.task_id}-${scan?.ip}`}>
            <Link to={`/scans/${scan?.task_id}`}>
              <div className="flex justify-around my-2">
                {scan?.ip}
                <TimeAgo timestamp={scan?.updated_at} />
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LastScans;
