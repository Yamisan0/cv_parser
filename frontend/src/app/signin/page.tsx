// src/app/login/page.tsx
"use client"; // Cette ligne indique que ce composant doit être rendu côté client

import { NextPage } from 'next';
import React, { useState, useCallback } from 'react';
import {
    Box,
    Button,
    Flex,
    Heading,
    Input,
    Stack,
    FormControl,
    FormLabel,
    ChakraProvider,
    useToast
} from '@chakra-ui/react';

const LoginPage: NextPage = () => {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [username, setUsername] = useState<string>('');
    const toast = useToast();

    const handleSubmit = useCallback(async (event: React.FormEvent) => {
        event.preventDefault();

        try {
            const response = await fetch('http://localhost:8000/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.token);
                console.log('Success:', data);
                toast({
                    title: "Connexion réussie.",
                    description: "Vous êtes maintenant connecté.",
                    status: "success",
                    duration: 5000,
                    isClosable: true,
                });
            } else {
                console.error('Error:', response.statusText);
                toast({
                    title: "Erreur de connexion.",
                    description: "Email ou pseudo déjà enregistré",
                    status: "error",
                    duration: 5000,
                    isClosable: true,
                });
            }
        } catch (error) {
            console.error('Error:', error);
            toast({
                title: "Erreur de serveur.",
                description: "Quelque chose s'est mal passé.",
                status: "error",
                duration: 5000,
                isClosable: true,
            });
        }
    }, [email, password, toast]);

    return (
        <ChakraProvider>
            <Flex minHeight="100vh" align="center" justify="center" bg="gray.50">
                <Box
                    maxWidth="400px"
                    width="full"
                    mt={8}
                    p={8}
                    borderRadius="8px"
                    boxShadow="lg"
                    bg="white"
                >
                    <Heading as="h2" size="xl" textAlign="center" mb="8">
                        Inscription
                    </Heading>
                    <form onSubmit={handleSubmit}>
                        <Stack spacing={4}>
                            <FormControl id="username">
                                <FormLabel>Nom d'utilisateur</FormLabel>
                                <Input
                                    type="username"
                                    placeholder="Username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </FormControl>
                            <FormControl id="email">
                                <FormLabel>Email</FormLabel>
                                <Input
                                    type="email"
                                    placeholder="Email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </FormControl>
                            <FormControl id="password">
                                <FormLabel>Mot de passe</FormLabel>
                                <Input
                                    type="password"
                                    placeholder="Mot de passe"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </FormControl>
                            <Button type="submit" colorScheme="teal" size="lg" width="full">
                                S'inscrire
                            </Button>
                        </Stack>
                    </form>
                </Box>
            </Flex>
        </ChakraProvider>
    );
};

export default LoginPage;
