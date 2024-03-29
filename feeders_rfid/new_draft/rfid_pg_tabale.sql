PGDMP                          w           bats    11.1    11.2     C           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            D           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            E           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            F           1262    16603    bats    DATABASE     �   CREATE DATABASE bats WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_Israel.1252' LC_CTYPE = 'English_Israel.1252';
    DROP DATABASE bats;
             postgres    false            �            1259    16656    rfid    TABLE     i  CREATE TABLE public.rfid (
    id integer NOT NULL,
    epc_id character varying,
    count character(99),
    rssi character(99),
    phase character(99),
    first_seen character(99),
    last_seen character(99),
    reader_number character(99),
    antenna_id character(99),
    adding_date timestamp with time zone DEFAULT (now() + '00:00:00'::interval)
);
    DROP TABLE public.rfid;
       public      
   power_user    false            �            1259    16663    rfid_id_seq    SEQUENCE     t   CREATE SEQUENCE public.rfid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.rfid_id_seq;
       public    
   power_user    false    208            G           0    0    rfid_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.rfid_id_seq OWNED BY public.rfid.id;
            public    
   power_user    false    209            �
           2604    16700    rfid id    DEFAULT     b   ALTER TABLE ONLY public.rfid ALTER COLUMN id SET DEFAULT nextval('public.rfid_id_seq'::regclass);
 6   ALTER TABLE public.rfid ALTER COLUMN id DROP DEFAULT;
       public    
   power_user    false    209    208            ?          0    16656    rfid 
   TABLE DATA               }   COPY public.rfid (id, epc_id, count, rssi, phase, first_seen, last_seen, reader_number, antenna_id, adding_date) FROM stdin;
    public    
   power_user    false    208   V       H           0    0    rfid_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.rfid_id_seq', 1442298, true);
            public    
   power_user    false    209            �
           2606    16717    rfid rfid_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.rfid
    ADD CONSTRAINT rfid_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.rfid DROP CONSTRAINT rfid_pkey;
       public      
   power_user    false    208            �
           2620    16732    rfid t_update_history    TRIGGER     v   CREATE TRIGGER t_update_history AFTER INSERT ON public.rfid FOR EACH ROW EXECUTE PROCEDURE public.f_update_history();
 .   DROP TRIGGER t_update_history ON public.rfid;
       public    
   power_user    false    208            ?      x������ � �     