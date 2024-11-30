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

