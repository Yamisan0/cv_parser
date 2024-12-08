"use client";

import React, { useState, useEffect, useRef } from "react";
import { NextPage } from "next";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { skillList } from "../lib/placeholder-data";
import TagInput from "../ui/jobform/modal_skills";

const ItemTypes = {
    ELEMENT: "element",
};

interface DraggableItem {
    name: string;
    category?: string;
}

interface SkillElementProps {
    name: string;
    category: Category;
    index: number;
    setSkills: React.Dispatch<React.SetStateAction<Skills>>;
}

function SkillElement({ name, category, index, setSkills }: SkillElementProps) {
    const handleClick = (newCategory: Category) => {
        console.log("Old :", category, "new : ", newCategory);
        if (category === newCategory) return;
        setSkills((prev) => {
            let newSkills = { ...prev };
            const cleanOldCategory = prev[category].filter(
                (value) => value != name
            );
            newSkills[category] = cleanOldCategory;
            const addNewCategory = [...prev[newCategory], name];
            newSkills[newCategory] = addNewCategory;
            return newSkills;
        });
    };
    return (
        <div
            key={index}
            className={`flex justify-between text-black cursor-move m-1 border border-gray-400 rounded-lg bg-gray-200`}
        >
            <p>{name}</p>
            <div className="button">
                <button
                    onClick={() => handleClick("fort")}
                    className=" p-0 m-0 text-green-100 hover:text-white border bg-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-800"
                ></button>
                <button
                    onClick={() => handleClick("moyen")}
                    type="button"
                    className="text-yellow-400 hover:text-white border bg-yellow-400 hover:bg-yellow-500 focus:ring-4 focus:outline-none focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-yellow-300 dark:text-yellow-300 dark:hover:text-white dark:hover:bg-yellow-400 dark:focus:ring-yellow-900"
                ></button>
                <button
                    onClick={() => handleClick("faible")}
                    type="button"
                    className=" text-red-700 hover:text-white border bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900 p-0 m-0"
                ></button>
            </div>
        </div>
    );
}

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

    return (
        <div className="flex h-screen bg-white justify-center text-black">
            <div className="flex-0 w-1/2 p-5 border-r border-gray-400">
                <input
                    type="text"
                    value={newElementName}
                    onChange={(e) => setNewElementName(e.target.value)}
                    placeholder="Nom de l'élément"
                    className="text-black mb-2 p-2 rounded border border-gray-400 w-full"
                />
                <div>
                    <button
                        onClick={() => handleAddElement("fort")}
                        className="inline-block mb-2 p-2 rounded bg-green-600 text-white border-none cursor-pointer mr-2"
                    >
                        Ajouter à Fort
                    </button>
                    <button
                        onClick={() => handleAddElement("moyen")}
                        className="inline-block mb-2 p-2 rounded bg-yellow-400 text-black border-none cursor-pointer mr-2"
                    >
                        Ajouter à Moyen
                    </button>
                    <button
                        onClick={() => handleAddElement("faible")}
                        className="inline-block mb-5 p-2 rounded bg-red-600 text-white border-none cursor-pointer"
                    >
                        Ajouter à Faible
                    </button>
                </div>
                <label className="text-black">Skills fort</label>
                <TagInput
                    setSkills={setSkills}
                    category="fort"
                    suggestions={["wewe", "lala"]}
                ></TagInput>
                <label className="text-black">Skills moyen</label>
                <TagInput
                    setSkills={setSkills}
                    category="moyen"
                    suggestions={["wewe", "lala"]}
                ></TagInput>
                <label className="text-black">Skills faible</label>
                <TagInput
                    setSkills={setSkills}
                    category="faible"
                    suggestions={["wewe", "lala"]}
                ></TagInput>
            </div>
            <div className="flex-0 w-1/2 flex flex-col p-5 overflow-auto">
                <div className="mb-5 bg-green-100 p-5 rounded">
                    <h2 className="text-black">Fort</h2>
                    {skills["fort"].map((name, index) => {
                        console.log("index = ", index, "name = ", name);
                        return SkillElement({
                            name,
                            category: "fort",
                            index,
                            setSkills,
                        });
                    })}
                </div>
                <div className="mb-5 bg-yellow-100 p-5 rounded">
                    <h2 className="text-black">Moyen</h2>
                    {skills.moyen.map((name, index) =>
                        SkillElement({
                            name,
                            category: "moyen",
                            index,
                            setSkills,
                        })
                    )}
                </div>
                <div className="bg-red-100 p-5 rounded">
                    <h2 className="text-black">Faible</h2>
                    {skills.faible.map((name, index) =>
                        SkillElement({
                            name,
                            category: "faible",
                            index,
                            setSkills,
                        })
                    )}
                </div>
            </div>
        </div>
    );
};

export default HomePage;
