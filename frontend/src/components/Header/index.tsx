import { FC, useState, useEffect, useRef } from "react";
import { BiHistory } from "react-icons/bi";
import { HiHome } from "react-icons/hi";
import { Link } from "react-router-dom";
import LastScans from "../LastScans";
import YourIp from "../YourIp";

const Header: FC = () => {
  const [isDropdownVisible, setDropdownVisible] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const toggleDropdown = () => {
    setDropdownVisible(!isDropdownVisible);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setDropdownVisible(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <header className="sticky w-full text-secondary text-lg h-24 bg-white shadow">
      <div className="h-full flex items-center justify-between container">
        <div className="flex gap-8 items-center">
          <Link to={"/"}>
            <HiHome size="1.75em" />
          </Link>
          <YourIp />
        </div>
        <div className="relative flex" ref={dropdownRef}>
          <BiHistory
            className="hover:cursor-pointer"
            size="1.75em"
            onClick={toggleDropdown}
          />
          {isDropdownVisible && <LastScans />}
        </div>
      </div>
    </header>
  );
};

export default Header;
