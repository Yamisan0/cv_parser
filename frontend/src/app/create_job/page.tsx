import React, { useState } from "react";
import Modal from "../components/Modal";
import HomePage from "../components/TagInput.tsx";

const suggestions = ["JavaScript", "React", "Node.js", "CSS", "HTML"];

const Home = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl mb-4">Tag Input with Modal</h1>
            <button
                onClick={openModal}
                className="bg-blue-500 text-white p-2 rounded"
            >
                Open Modal
            </button>
            <Modal isOpen={isModalOpen} onClose={closeModal}>
                <h2 className="text-xl mb-4">Add Tags</h2>
                <HomePage suggestions={suggestions} />
            </Modal>
        </div>
    );
};

export default Home;
