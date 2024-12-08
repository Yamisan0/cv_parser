"use client";

import React, { useState, useEffect, useRef } from "react";
import { NextPage } from "next";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { skillList } from "../lib/placeholder-data";
import TagInput from "../ui/jobform/modal_skills";
import localFont from "next/font/local";

// Font files can be colocated inside of `pages`
const myFont = localFont({ src: "./Iliad-Regular.otf" });

const defaultSkills: Skills = {
    fort: [],
    moyen: [],
    faible: [],
};

const HomePage: NextPage = () => {
    const [availableElements, setAvailableElements] =
        useState<string[]>(skillList);
    const [skills, setSkills] = useState<Skills>(defaultSkills);
    const [newElementName, setNewElementName] = useState("");

    const handleAddElement = (category: Category) => {
        console.log(
            "ajout de l'élément : ",
            newElementName,
            "Catégorie : ",
            category
        );
        if (newElementName.trim() !== "") {
            setSkills((prev) => {
                const newSkills: Skills = { ...prev };
                if (!newSkills[category]) newSkills[category] = [];
                newSkills[category] = [...newSkills[category], newElementName];
                return newSkills;
            });
            setNewElementName("");
        }
    };

    function handleForm() {
        // Envoyer l'objet skills
    }

    return (
        <div className=" w-[100%] flex flex-col items-center ">
            <div className="p-4 w-1/2 m-10 flex flex-col items-center border-4 border-gray-500 rounded-xl border-solid bg-white shadow-md shadow-white">
                <label className="text-blue-gray-600">Titre du poste</label>
                <input
                    className="flex flex-wrap border p-2 rounded"
                    type="text"
                    placeholder="Titre du Job"
                />
                <label className="text-blue-gray-600">Skills fort</label>
                <TagInput
                    setSkills={setSkills}
                    category="fort"
                    suggestions={["wewe", "lala"]}
                ></TagInput>
                <label className="text-blue-gray-600">Skills moyen</label>
                <TagInput
                    setSkills={setSkills}
                    category="moyen"
                    suggestions={["wewe", "lala"]}
                ></TagInput>
                <label className="text-blue-gray-600">Skills faible</label>
                <TagInput
                    setSkills={setSkills}
                    category="faible"
                    suggestions={["wewe", "lala"]}
                ></TagInput>
                <button
                    type="button"
                    className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
                    onClick={handleForm}
                >
                    Valider
                </button>
            </div>
        </div>
    );
};

export default HomePage;
