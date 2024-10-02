import React, { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-gray-800 p-4 flex items-center justify-between">
      <div className="text-white text-2xl ml-3">HealthSOS</div>
      <div className="md:hidden" onClick={toggleMenu}>
        <div className={`h-1 w-6 my-1 bg-white transition transform ${isOpen ? 'rotate-45 translate-y-2' : ''}`}></div>
        <div className={`h-1 w-6 my-1 bg-white transition ${isOpen ? 'opacity-0' : ''}`}></div>
        <div className={`h-1 w-6 my-1 bg-white transition transform ${isOpen ? '-rotate-45 -translate-y-2' : ''}`}></div>
      </div>
      <ul className={`fixed top-0 right-0 h-40 w-full bg-gray-800 flex flex-col items-center justify-center p-4 space-y-4 transform ${isOpen ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-300 ease-in-out md:relative md:flex md:flex-row md:space-x-6 md:translate-x-0`}>
        <li className="absolute top-4 right-4 md:hidden"><button onClick={toggleMenu} className="text-white">X</button></li>
        <li><a href="" className="text-white flex flex-col items-center md:flex-row"><i className="fas fa-home block md:hidden"></i><span className="hidden md:block ml-3">Home</span></a></li>
        <li><a href="" className="text-white flex flex-col items-center md:flex-row"><i className="fas fa-info-circle block md:hidden"></i><span className="hidden md:block ml-3">About</span></a></li>
        <li><a href="" className="text-white flex flex-col items-center md:flex-row"><i className="fas fa-concierge-bell block md:hidden"></i><span className="hidden md:block ml-3">Services</span></a></li>
        <li><a href="" className="text-white flex flex-col items-center md:flex-row"><i className="fas fa-envelope block md:hidden"></i><span className="hidden md:block ml-3">Contact</span></a></li>
      </ul>
    </nav>
  );
};

export default Navbar;
