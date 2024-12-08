import React, { useState, useEffect, useRef } from "react";

interface TagInputProps {
    suggestions: string[];
    category: Category;
    setSkills: React.Dispatch<React.SetStateAction<Skills>>;
}

const TagInput = ({ suggestions, category, setSkills }: TagInputProps) => {
    const [tags, setTags] = useState<string>([]);
    const [input, setInput] = useState("");
    const [filteredSuggestions, setFilteredSuggestions] = useState(suggestions);
    const [activeSuggestionIndex, setActiveSuggestionIndex] = useState(-1);
    const suggestionsRef = useRef(null);

    const handleAddElement = (category: Category, name: string) => {
        console.log("ajout de l'élément : ", name, "Catégorie : ", category);
        if (name.trim() !== "") {
            setSkills((prev) => {
                const newSkills: Skills = { ...prev };
                if (!newSkills[category]) newSkills[category] = [];
                newSkills[category] = [...newSkills[category], name];
                return newSkills;
            });
        }
    };
    function removeElement(category: Category, name: string) {
        setSkills((prev) => {
            const newSkills: Skills = { ...prev };
            newSkills[category] = newSkills[category].filter(
                (skill) => skill !== name
            );
            return newSkills;
        });
    }

    useEffect(() => {
        setFilteredSuggestions(
            suggestions.filter((suggestion) =>
                suggestion.toLowerCase().includes(input.toLowerCase())
            )
        );
    }, [input, suggestions]);

    const addTag = (tag: string) => {
        console.log("add skill = ", tag);
        if (!tags.includes(tag) && tag.trim() !== "") {
            setTags([...tags, tag]);
            setInput("");
            handleAddElement(category, tag);
        }
    };

    const removeTag = (tag: string) => {
        setTags(tags.filter((t) => t !== tag));
        removeElement(category, tag);
    };

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleInputKeyDown = (e) => {
        if (e.key === "Enter") {
            console.log("enter key pressed")
            if (activeSuggestionIndex >= 0) {
                addTag(filteredSuggestions[activeSuggestionIndex]);
                setActiveSuggestionIndex(activeSuggestionIndex - 1);
            } else if (input.trim() !== "") {
                console.log("enter key not in suggestion tag = ", input)
                addTag(input);
            }
        } else if (e.key === "ArrowDown") {
            if (activeSuggestionIndex < filteredSuggestions.length - 1) {
                setActiveSuggestionIndex(activeSuggestionIndex + 1);
            }
        } else if (e.key === "ArrowUp") {
            if (activeSuggestionIndex > 0) {
                setActiveSuggestionIndex(activeSuggestionIndex - 1);
            }
        }
    };

    const handleSuggestionClick = (suggestion) => {
        addTag(suggestion);
    };

    return (
        <div className="w-full max-w-lg  mt-4 text-black">
            <div className="flex flex-wrap border p-2 rounded">
                {tags.map((tag: string) => (
                    <div
                        key={tag}
                        className="flex items-center bg-gray-200 p-1 m-1 rounded"
                    >
                        {tag}
                        <button
                            onClick={() => removeTag(tag)}
                            className="ml-2 text-red-600 hover:text-red-800"
                        >
                            &times;
                        </button>
                    </div>
                ))}
                <input
                    type="text"
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleInputKeyDown}
                    className="flex-grow p-1 m-1 outline-none"
                    placeholder="Add skill..."
                />
            </div>
            {input && (
                <div
                    ref={suggestionsRef}
                    className="border rounded mt-2 absolute bg-white shadow-lg max-h-40 w-full max-w-lg overflow-y-auto z-10"
                >
                    {filteredSuggestions.map((suggestion, index) => (
                        <div
                            key={suggestion}
                            onClick={() => handleSuggestionClick(suggestion)}
                            className={`cursor-pointer p-2 hover:bg-gray-200 ${
                                index === activeSuggestionIndex
                                    ? "bg-gray-300"
                                    : ""
                            }`}
                        >
                            {suggestion}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default TagInput;
