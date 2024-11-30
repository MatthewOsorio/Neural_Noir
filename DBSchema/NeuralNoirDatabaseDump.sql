--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: biometricfeedback; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.biometricfeedback (
    feedbackid uuid NOT NULL,
    starttime time without time zone,
    endtime time without time zone,
    stddeviation real,
    temperature real,
    heartrate integer,
    skinconduction real,
    outlier boolean,
    sessionid uuid
);


ALTER TABLE public.biometricfeedback OWNER TO postgres;

--
-- Name: gamesession; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gamesession (
    sessionid uuid NOT NULL,
    sessionstarttime timestamp without time zone,
    sessionendtime timestamp without time zone,
    ending integer
);


ALTER TABLE public.gamesession OWNER TO postgres;

--
-- Name: interaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.interaction (
    interactionid uuid NOT NULL,
    starttime time without time zone,
    endtime time without time zone,
    userinput character varying(255),
    generatedresponse character varying(255),
    discrepancy boolean,
    sessionid uuid
);


ALTER TABLE public.interaction OWNER TO postgres;

--
-- Data for Name: biometricfeedback; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.biometricfeedback (feedbackid, starttime, endtime, stddeviation, temperature, heartrate, skinconduction, outlier, sessionid) FROM stdin;
\.


--
-- Data for Name: gamesession; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gamesession (sessionid, sessionstarttime, sessionendtime, ending) FROM stdin;
11a5d254-1b3c-4bee-96c8-332f9f49650b	2024-11-26 23:11:04	\N	\N
a69c94a1-d9dc-4dd3-ae3f-c198ae522459	2024-11-26 23:12:20	\N	\N
7ee1e28c-5e9d-44db-a911-eecbe7e5f850	2024-11-26 23:13:49	\N	\N
c76a929a-4673-4fc1-a35c-135fda66cfae	2024-11-27 13:32:04	\N	\N
1e89d272-c2e0-4912-9761-41c30eed6167	2024-11-27 14:45:00	\N	\N
f7a75f84-c7d6-42ca-946e-0e226299ebd5	2024-11-27 14:46:43	\N	\N
172891ba-ca33-41d9-818e-85c5f183130a	2024-11-27 14:47:34	\N	\N
2d802783-bdce-4ee2-aa3d-6d6fd119dc7c	2024-11-27 14:52:23	\N	\N
f5967100-ec26-4454-a0d1-1677bbb18895	2024-11-27 14:56:13	\N	\N
8940e335-3fde-4084-94e6-1537bce6d3d4	2024-11-27 14:59:10	\N	\N
e5410695-ded0-4040-a560-d45e36f0238e	2024-11-27 19:35:56	\N	\N
7b026d58-8991-4e39-91dc-c58be5b6391f	2024-11-28 15:27:30	\N	\N
677a0aa4-c04c-4120-be72-0667494d5fe6	2024-11-28 17:07:27	\N	\N
7cb45787-e117-4954-a21a-63d6d4311064	2024-11-28 23:03:28	\N	\N
fcd7f684-be09-4a69-894b-d587f16431b1	2024-11-28 23:03:40	\N	\N
b82dd3d0-7e10-4b35-bb17-71cb68bd8918	2024-11-28 23:05:27	\N	\N
01b7c6e0-2cc8-4843-aad3-2ba10fe12928	2024-11-29 12:23:07	\N	\N
00d63c20-e4f3-4a94-869c-81eaab483551	2024-11-29 12:27:11	\N	\N
0c782a2d-8039-4e2b-9b3f-7292552e3221	2024-11-29 12:27:48	\N	\N
104eb162-d621-461b-8703-a5fd0e0c618a	2024-11-29 12:28:39	\N	\N
\.


--
-- Data for Name: interaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.interaction (interactionid, starttime, endtime, userinput, generatedresponse, discrepancy, sessionid) FROM stdin;
64dbc1a8-b103-4755-9dc3-529b603dd592	10:15:17	10:16:01	I was at the party	where were you last night	\N	\N
c3ffb92e-6e8e-4554-8e33-09c8597a4ffe	10:15:17	10:16:01	Yes my mom	Do you have an alibi?	\N	\N
4e4f7d71-46dc-4d6d-b097-7ff70a085582	14:47:37	14:47:42	I was at the party with my girlfriend.	\N	\N	172891ba-ca33-41d9-818e-85c5f183130a
fa2a1698-829a-45b9-87d3-e094c60209fd	14:48:02	14:48:06	Why are you so mean to me?	Alright, let's not play around. What's your girlfriend's name? How long you've been together? And don't think I won't check on your story. Why would she alibi for a lowly scum like yourself who was smitten with hatred for the victim? Spit it out.	\N	172891ba-ca33-41d9-818e-85c5f183130a
14b8af06-390c-4f50-8c17-9a77b1fe3e52	14:52:26	14:52:29	I was at the party getting drunk with my homies.	\N	\N	2d802783-bdce-4ee2-aa3d-6d6fd119dc7c
c02adcca-fdd6-4379-979d-6227858881c0	14:56:16	14:56:22	I was at the company party having beer	\N	\N	f5967100-ec26-4454-a0d1-1677bbb18895
e1ae35c7-c5fe-4c41-9e1d-c6e994d1579a	14:56:33	14:56:40	I was with my friends, so I don't know we got pretty crazy	I see, getting a bit tipsy were you? Anyone who can vouch for you during the time the lights went off? Think carefully.	\N	f5967100-ec26-4454-a0d1-1677bbb18895
3ee05809-4279-44c3-b736-0d1522774002	14:59:13	14:59:18	I was at the company party in the bathroom.	Where were you last night?	\N	8940e335-3fde-4084-94e6-1537bce6d3d4
72042306-c483-4368-9cba-269ab73a9862	19:36:00	19:36:05	I was at home. I was not at the party.	Where were you last night?	\N	e5410695-ded0-4040-a560-d45e36f0238e
aa16a5d5-9f30-4eb5-8203-584eb250901e	15:27:33	15:27:38	I was at the party for the company.	Where were you last night?	\N	7b026d58-8991-4e39-91dc-c58be5b6391f
d4fe47f3-b22c-476c-b74c-3c5249258083	15:27:52	15:27:56	I don't know, we just, we just butted heads a lot.	That's right.. you were, along with a lot of other people. However, you didn't like the CEO did you? You had a grudge, a motive to harm him. Why was that?	\N	7b026d58-8991-4e39-91dc-c58be5b6391f
1f75dbde-a3de-4c56-b9c0-db8373010791	15:28:11	15:28:15	He had sex with my ex-wife	Just butted heads, huh? That's one way to put it. You despised the man. It's got to be more than a few disagreements. What was the real reason? What did he do to you?	\N	7b026d58-8991-4e39-91dc-c58be5b6391f
ae5c613b-2e8f-4901-8b6e-5db790132ef2	15:28:33	15:28:39	I don't know. I just got really depressed	Well, well, well... that sounds like a hell of a motive to me. A man that not only screwed you over at work but also in your personal life. Tell me, how did you feel when you found out? Angry? Betrayed? Vengeful?	\N	7b026d58-8991-4e39-91dc-c58be5b6391f
1899e1dc-80c5-46cf-94a0-6d99c5bf3bb8	15:28:57	15:29:03	What are you assuming? Are you trying to say I did something to him?	Depressed, huh? That's a heavy word. Sometimes people do wild things when they're in a dark place. Did the depression lead you to anger? To revenge? Were you waiting for the right moment to make him pay for what he did to you?	\N	7b026d58-8991-4e39-91dc-c58be5b6391f
41b4224d-d04a-446d-983e-9e89da03a66b	15:29:21	15:29:26	No, I didn't. I didn't like the guy, but I didn't want to kill him.	I'm not assuming anything, I'm just putting the pieces of the puzzle together. And so far, the picture it's forming points a big fat curse filled finger at you. You had a motive and an opportunity to harm him. Did you?	\N	7b026d58-8991-4e39-91dc-c58be5b6391f
4fae3d4c-ee33-4dfe-a51d-5bd17c1d61f5	23:03:44	23:03:47	I was at home.	Where were you last night?	\N	fcd7f684-be09-4a69-894b-d587f16431b1
3a6fcab0-6e96-4c33-a7a6-51714abdb631	12:28:01	12:28:06	I don't know what you're talking about, man. I don't know who you are.	[**Aggressive Interrogation Style**]\n\n*slams the table* Alright, let's cut to the chase. What's your name? You've been in here a while, so I assume you know what this is about, right?	\N	0c782a2d-8039-4e2b-9b3f-7292552e3221
\.


--
-- Name: biometricfeedback biometricfeedback_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.biometricfeedback
    ADD CONSTRAINT biometricfeedback_pkey PRIMARY KEY (feedbackid);


--
-- Name: gamesession gamesession_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gamesession
    ADD CONSTRAINT gamesession_pkey PRIMARY KEY (sessionid);


--
-- Name: interaction interaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interaction
    ADD CONSTRAINT interaction_pkey PRIMARY KEY (interactionid);


--
-- Name: biometricfeedback biometricfeedback_sessionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.biometricfeedback
    ADD CONSTRAINT biometricfeedback_sessionid_fkey FOREIGN KEY (sessionid) REFERENCES public.gamesession(sessionid);


--
-- Name: interaction interaction_sessionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interaction
    ADD CONSTRAINT interaction_sessionid_fkey FOREIGN KEY (sessionid) REFERENCES public.gamesession(sessionid);


--
-- PostgreSQL database dump complete
--

