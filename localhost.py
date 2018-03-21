3
㤱Z&h  �               @   s�  d Z ddddgZddlZddlZddlZddlZddlZddl	Z	ddl
Z
ddlZddlZddlZddlZddlZddlZddlZddlZddlZddlZddlZddlmZ ed� ejd	� ed
�Zed� dZdZG dd� dej�ZG dd� dej�Z G dd� de �Z!dd� Z"da#dd� Z$dd� Z%G dd� de!�Z&e edddfdd�Z'e(dk�r�ej)� Z*e*j+dddd � e*j+d!d"dd#dd$� e*j+d%d&e,e�e-d'dd(� e*j.� Z/e/j0�r�e&Z1ne!Z1e'e1e/j2e/j3d)� dS )*z1.0�
HTTPServer�BaseHTTPRequestHandler�SimpleHTTPRequestHandler�CGIHTTPRequestHandler�    N)�
HTTPStatuszm
 ::::::::::::::::::::::::::::::::

 [+] Webserver

 [+] Coded By: EdSec

 ::::::::::::::::::::::::::::::::

�   z% [+] Digite a porta que deseja usar: � a�  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: %(code)d</p>
        <p>Message: %(message)s.</p>
        <p>Error code explanation: %(code)s - %(explain)s.</p>
    </body>
</html>
ztext/html;charset=utf-8c               @   s   e Zd ZdZdd� ZdS )r   r   c             C   s4   t jj| � | jd d� \}}tj|�| _|| _d S )N�   )�socketserver�	TCPServer�server_bind�server_address�socketZgetfqdn�server_name�server_port)�self�host�port� r   �%/storage/emulated/legacy/localhost.pyr   H   s    zHTTPServer.server_bindN)�__name__�
__module__�__qualname__Zallow_reuse_addressr   r   r   r   r   r   D   s   c               @   s  e Zd Zdejj� d  Zde Ze	Z
eZdZdd� Zdd� Zd	d
� Zdd� Zd?dd�Zd@dd�ZdAdd�Zdd� Zdd� Zdd� ZdBdd�Zdd� Zdd � Zd!d"� ZdCd#d$�Zd%d&� Zd'd(d)d*d+d,d-gZdd.d/d0d1d2d3d4d5d6d7d8d9gZd:d;� Z d<Z!e"j#j$Z%d=d>� e&j'j(� D �Z)dS )Dr   zPython/r   z	BaseHTTP/zHTTP/0.9c             C   s�  d | _ | j | _}d| _t| jd�}|jd�}|| _|j� }t	|�dk�r|\}}}yZ|d d� dkrjt
�|jdd�d }|jd	�}t	|�d
kr�t
�t|d �t|d �f}W n* t
tfk
r�   | jtjd| � dS X |dkr�| jdkr�d| _|dk�rr| jtjd| � dS n^t	|�d
k�rR|\}}d| _|dk�rr| jtjd| � dS n |�s\dS | jtjd| � dS |||  | _ | _| _ytjj| j| jd�| _W nr tjjk
�r� } z| jtjdt|�� dS d }~X n: tjjk
�r } z| jtjdt|�� dS d }~X nX | jjdd�}	|	j� dk�r:d| _n |	j� dk�rZ| jdk�rZd| _| jjdd�}
|
j� dk�r�| jdk�r�| jdk�r�| j� �s�dS dS )NTz
iso-8859-1z
�   �   zHTTP/�/r   �.r	   r   zBad request version (%r)FzHTTP/1.1zInvalid HTTP version (%s)ZGETzBad HTTP/0.9 request type (%r)zBad request syntax (%r))Z_classzLine too longzToo many headers�
Connection� �closez
keep-aliveZExpectz100-continue)r   r   )r	   r   )�command�default_request_version�request_version�close_connection�str�raw_requestline�rstrip�requestline�split�len�
ValueError�int�
IndexError�
send_errorr   ZBAD_REQUEST�protocol_versionZHTTP_VERSION_NOT_SUPPORTED�path�http�clientZparse_headers�rfile�MessageClass�headersZLineTooLongZREQUEST_HEADER_FIELDS_TOO_LARGEZHTTPException�get�lower�handle_expect_100)r   �versionr'   �wordsr    r/   Zbase_version_numberZversion_number�errZconntypeZexpectr   r   r   �parse_requestV   s�    












z$BaseHTTPRequestHandler.parse_requestc             C   s   | j tj� | j�  dS )NT)�send_response_onlyr   ZCONTINUE�end_headers)r   r   r   r   r7   �   s    z(BaseHTTPRequestHandler.handle_expect_100c             C   s�   y�| j jd�| _t| j�dkr@d| _d| _d| _| jtj	� d S | jsPd| _
d S | j� s\d S d| j }t| |�s�| jtjd| j � d S t| |�}|�  | jj�  W n4 tjk
r� } z| jd|� d| _
d S d }~X nX d S )Ni  i   r   TZdo_zUnsupported method (%r)zRequest timed out: %r)r2   �readliner%   r)   r'   r"   r    r-   r   ZREQUEST_URI_TOO_LONGr#   r;   �hasattr�NOT_IMPLEMENTED�getattr�wfile�flushr   Ztimeout�	log_error)r   Zmname�method�er   r   r   �handle_one_request�   s4    


z)BaseHTTPRequestHandler.handle_one_requestc             C   s&   d| _ | j�  x| j s | j�  qW d S )NT)r#   rG   )r   r   r   r   �handle�   s    zBaseHTTPRequestHandler.handleNc             C   s
  y| j | \}}W n tk
r.   d\}}Y nX |d kr<|}|d krH|}| jd||� | j||� | jdd� d }|dkr�|tjtjtjfkr�| j	|t
j|dd�t
j|dd�d� }|jd	d
�}| jd| j� | jdtt|��� | j�  | jdko�|�r| jj|� d S )N�???zcode %d, message %sr   r   ��   F)�quote)�code�message�explainzUTF-8�replacezContent-TypezContent-LengthZHEAD)rI   rI   )�	responses�KeyErrorrD   �send_response�send_headerr   Z
NO_CONTENTZRESET_CONTENTZNOT_MODIFIED�error_message_format�html�escape�encode�error_content_typer+   r)   r=   r    rB   �write)r   rL   rM   rN   ZshortmsgZlongmsgZbodyZcontentr   r   r   r-   �   s4    
z!BaseHTTPRequestHandler.send_errorc             C   s:   | j |� | j||� | jd| j� � | jd| j� � d S )NZServerZDate)�log_requestr<   rS   �version_string�date_time_string)r   rL   rM   r   r   r   rR   �   s    
z$BaseHTTPRequestHandler.send_responsec             C   sd   | j dkr`|d kr0|| jkr,| j| d }nd}t| d�s@g | _| jjd| j||f jdd�� d S )NzHTTP/0.9r   r   �_headers_bufferz
%s %d %s
zlatin-1�strict)r"   rP   r?   r]   �appendr.   rW   )r   rL   rM   r   r   r   r<   �   s    


z)BaseHTTPRequestHandler.send_response_onlyc             C   sl   | j dkr6t| d�sg | _| jjd||f jdd�� |j� dkrh|j� dkrVd| _n|j� d	krhd
| _d S )NzHTTP/0.9r]   z%s: %s
zlatin-1r^   Z
connectionr   Tz
keep-aliveF)r"   r?   r]   r_   rW   r6   r#   )r   Zkeyword�valuer   r   r   rS     s    

z"BaseHTTPRequestHandler.send_headerc             C   s"   | j dkr| jjd� | j�  d S )NzHTTP/0.9s   
)r"   r]   r_   �flush_headers)r   r   r   r   r=     s    
z"BaseHTTPRequestHandler.end_headersc             C   s(   t | d�r$| jjdj| j�� g | _d S )Nr]   �    )r?   rB   rY   �joinr]   )r   r   r   r   ra     s    
z$BaseHTTPRequestHandler.flush_headers�-c             C   s.   t |t�r|j}| jd| jt|�t|�� d S )Nz
"%s" %s %s)�
isinstancer   r`   �log_messager'   r$   )r   rL   �sizer   r   r   rZ     s    
z"BaseHTTPRequestHandler.log_requestc             G   s   | j |f|��  d S )N)rf   )r   �format�argsr   r   r   rD     s    z BaseHTTPRequestHandler.log_errorc             G   s*   t jjd| j� | j� d || f � d S )Nz
 [+]>> %s = %s] %s
z
 [+]>> )�sys�stderrrY   �address_string�log_date_time_string)r   rh   ri   r   r   r   rf   "  s    z"BaseHTTPRequestHandler.log_messagec             C   s   | j d | j S )Nr   )�server_version�sys_version)r   r   r   r   r[   '  s    z%BaseHTTPRequestHandler.version_stringc             C   s    |d krt j � }tjj|dd�S )NT)Zusegmt)�time�emailZutilsZ
formatdate)r   Z	timestampr   r   r   r\   *  s    z'BaseHTTPRequestHandler.date_time_stringc          	   C   sB   t j � }t j|�\	}}}}}}}}	}
d|| j| ||||f }|S )Nz%02d/%3s/%04d %02d:%02d:%02d)rp   Z	localtime�	monthname)r   ZnowZyearZmonthZdayZhhZmmZss�x�y�z�sr   r   r   rm   /  s
    z+BaseHTTPRequestHandler.log_date_time_stringZMonZTueZWedZThuZFriZSatZSunZJanZFebZMarZAprZMayZJunZJulZAugZSepZOctZNovZDecc             C   s
   | j d S )Nr   )�client_address)r   r   r   r   rl   <  s    z%BaseHTTPRequestHandler.address_stringzHTTP/1.0c             C   s   i | ]}|j |jf|�qS r   )ZphraseZdescription)�.0�vr   r   r   �
<dictcomp>E  s   z!BaseHTTPRequestHandler.<dictcomp>)NN)N)N)rd   rd   )N)*r   r   r   rj   r8   r(   ro   �__version__rn   �DEFAULT_ERROR_MESSAGErT   �DEFAULT_ERROR_CONTENT_TYPErX   r!   r;   r7   rG   rH   r-   rR   r<   rS   r=   ra   rZ   rD   rf   r[   r\   rm   Zweekdaynamerr   rl   r.   r0   r1   ZHTTPMessager3   r   Z__members__�valuesrP   r   r   r   r   r   O   s<   O
 



c               @   sx   e Zd Zde Zdd� Zdd� Zdd� Zdd	� Zd
d� Z	dd� Z
dd� ZejsVej�  ejj� Zejddddd�� dS )r   zSimpleHTTP/c          
   C   s.   | j � }|r*z| j|| j� W d |j�  X d S )N)�	send_head�copyfilerB   r   )r   �fr   r   r   �do_GETP  s
    zSimpleHTTPRequestHandler.do_GETc             C   s   | j � }|r|j�  d S )N)r   r   )r   r�   r   r   r   �do_HEADX  s    z SimpleHTTPRequestHandler.do_HEADc       	      C   sx  | j | j�}d }tjj|�r�tjj| j�}|jjd�s�| jt	j
� |d |d |d d |d |d f}tjj|�}| jd|� | j�  d S x6dD ]$}tjj||�}tjj|�r�|}P q�W | j|�S | j|�}yt|d
�}W n$ tk
�r    | jt	jd� d S X yZ| jt	j� | jd|� tj|j� �}| jdt|d �� | jd| j|j�� | j�  |S    |j�  � Y nX d S )Nr   r   r   r	   r   �   ZLocation�
index.html�	index.htmZrbzFile not foundzContent-typezContent-Length�   zLast-Modified)r�   r�   )�translate_pathr/   �os�isdir�urllib�parseZurlsplit�endswithrR   r   ZMOVED_PERMANENTLYZ
urlunsplitrS   r=   rc   �exists�list_directory�
guess_type�open�OSErrorr-   �	NOT_FOUND�OK�fstat�filenor$   r\   �st_mtimer   )	r   r/   r�   ZpartsZ	new_partsZnew_url�indexZctypeZfsr   r   r   r   ]  sF    


z"SimpleHTTPRequestHandler.send_headc             C   s�  yt j|�}W n" tk
r0   | jtjd� d S X |jdd� d� g }ytjj	| j
dd�}W n  tk
r|   tjj	|�}Y nX tj|dd�}tj� }d	| }|jd
� |jd� |jd| � |jd| � |jd| � |jd� x~|D ]v}t j
j||�}| }	}
t j
j|��r"|d }	|d }
t j
j|��r8|d }	|jdtjj|
dd�tj|	dd�f � q�W |jd� |jd� dj|�j|d�}tj� }|j|� |jd� | jtj� | jdd| � | jdtt|��� | j�  |S )NzNo permission to list directoryc             S   s   | j � S )N)r6   )�ar   r   r   �<lambda>�  s    z9SimpleHTTPRequestHandler.list_directory.<locals>.<lambda>)�key�surrogatepass)�errorsF)rK   u   Listando diretório  %szZ<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">z&<html>
<title>localhost</title>
<head>z@<meta http-equiv="Content-Type" content="text/html; charset=%s">z<title>%s</title>
</head>z<body>
<h1>%s</h1>z	<hr>
<ul>r   �@z<li><a href="%s">%s</a></li>zT<hr><h5>Github: <a href="https://github.com/EdSec">https://github.com/EdSec</a></h5>z</ul>
<hr>
</body>
</html>
�
�surrogateescaper   zContent-typeztext/html; charset=%szContent-Length) r�   �listdirr�   r-   r   r�   �sortr�   r�   �unquoter/   �UnicodeDecodeErrorrU   rV   rj   �getfilesystemencodingr_   rc   r�   �islinkrK   rW   �io�BytesIOrY   �seekrR   r�   rS   r$   r)   r=   )r   r/   �list�rZdisplaypathZenc�title�name�fullnameZdisplaynameZlinknameZencodedr�   r   r   r   r�   �  s^    








z'SimpleHTTPRequestHandler.list_directoryc             C   s�   |j dd�d }|j dd�d }|j� jd�}ytjj|dd�}W n  tk
rb   tjj|�}Y nX tj|�}|j d�}t	d |�}t
j� }x8|D ]0}t
jj|�s�|t
jt
jfkr�q�t
jj||�}q�W |r�|d7 }|S )N�?r   r   �#r   r�   )r�   )r(   r&   r�   r�   r�   r�   r�   �	posixpath�normpath�filterr�   �getcwdr/   �dirname�curdir�pardirrc   )r   r/   Ztrailing_slashr9   Zwordr   r   r   r�   �  s$    



z'SimpleHTTPRequestHandler.translate_pathc             C   s   t j||� d S )N)�shutilZcopyfileobj)r   �sourceZ
outputfiler   r   r   r�   �  s    z!SimpleHTTPRequestHandler.copyfilec             C   sL   t j|�\}}|| jkr"| j| S |j� }|| jkr>| j| S | jd S d S )Nr   )r�   �splitext�extensions_mapr6   )r   r/   �baseZextr   r   r   r�   �  s    



z#SimpleHTTPRequestHandler.guess_typezapplication/octet-streamz
text/plain)r   z.pyz.cz.hN)r   r   r   r{   rn   r�   r�   r   r�   r�   r�   r�   �	mimetypesZinitedZinitZ	types_map�copyr�   �updater   r   r   r   r   K  s    &3

c       	      C   s�   | j d�\} }}tjj| �} | jd�}g }x<|d d� D ],}|dkrN|j�  q8|r8|dkr8|j|� q8W |r�|j� }|r�|dkr�|j�  d}q�|dkr�d}nd}|r�dj||f�}ddj|� |f}dj|�}|S )Nr�   r   r   z..r   r   �����)�	partitionr�   r�   r�   r(   �popr_   rc   )	r/   �_�query�
path_partsZ
head_parts�partZ	tail_partZ	splitpath�collapsed_pathr   r   r   �_url_collapse_path�  s.    


r�   c              C   sp   t rt S ydd l} W n tk
r(   dS X y| jd�d a W n. tk
rj   dtdd� | j� D �� a Y nX t S )Nr   r   �nobodyr	   c             s   s   | ]}|d  V  qdS )r	   Nr   )rx   rs   r   r   r   �	<genexpr>  s    znobody_uid.<locals>.<genexpr>r�   )r�   �pwd�ImportError�getpwnamrQ   �maxZgetpwall)r�   r   r   r   �
nobody_uid  s     r�   c             C   s   t j| t j�S )N)r�   �access�X_OK)r/   r   r   r   �
executable  s    r�   c               @   sR   e Zd Zeed�ZdZdd� Zdd� Zdd� Z	d	d
gZ
dd� Zdd� Zdd� ZdS )r   �forkr   c             C   s$   | j � r| j�  n| jtjd� d S )NzCan only POST to CGI scripts)�is_cgi�run_cgir-   r   r@   )r   r   r   r   �do_POST  s
    
zCGIHTTPRequestHandler.do_POSTc             C   s   | j � r| j� S tj| �S d S )N)r�   r�   r   r   )r   r   r   r   r   "  s    zCGIHTTPRequestHandler.send_headc             C   sP   t | j�}|jdd�}|d |� ||d d �  }}|| jkrL||f| _dS dS )Nr   r   TF)r�   r/   �find�cgi_directories�cgi_info)r   r�   Zdir_sep�head�tailr   r   r   r�   (  s    


zCGIHTTPRequestHandler.is_cgiz/cgi-binz/htbinc             C   s   t |�S )N)r�   )r   r/   r   r   r   �is_executable4  s    z#CGIHTTPRequestHandler.is_executablec             C   s   t jj|�\}}|j� dkS )N�.py�.pyw)r�   r�   )r�   r/   r�   r6   )r   r/   r�   r�   r   r   r   �	is_python7  s    zCGIHTTPRequestHandler.is_pythonc       )      C   s�  | j \}}|d | }|jdt|�d �}x`|dkr�|d |� }||d d � }| j|�}tjj|�r�|| }}|jdt|�d �}q,P q,W |jd�\}}}	|jd�}|dkr�|d |� ||d �  }
}n
|d }
}|d |
 }| j|�}tjj|��s| j	t
jd| � d S tjj|��s2| j	t
jd| � d S | j|�}| j�sL| �rn| j|��sn| j	t
jd| � d S tjtj�}| j� |d	< | jj|d
< d|d< | j|d< t| jj�|d< | j|d< tjj|�}||d< | j|�|d< ||d< |	�r�|	|d< | jd |d< | jj d�}|�r�|j!� }t|�dk�r�dd l"}dd l#}|d |d< |d j$� dk�r�y"|d j%d�}|j&|�j'd�}W n |j(t)fk
�r�   Y n&X |j!d�}t|�dk�r�|d |d< | jj d�d k�r�| jj*� |d< n| jd |d< | jj d�}|�r||d< | jj d �}|�r"||d!< g }xN| jj+d"�D ]>}|d d� d#k�rZ|j,|j-� � n||d$d � j!d%� }�q4W d%j.|�|d&< | jj d'�}|�r�||d(< t/d | jj0d)g ��}d*j.|�}|�r�||d+< xd<D ]}|j1|d� �q�W | j2t
j3d-� | j4�  |	j5d.d/�}| j�r.|
g}d0|k�r*|j,|� t6� }| j7j8�  tj9� }|dk�r�tj:|d�\}}x0t;j;| j<gg g d�d �r�| j<j=d��s^P �q^W |�r�| j>d1|� d S y\ytj?|� W n t@k
�r�   Y nX tjA| j<jB� d� tjA| j7jB� d� tjC|||� W n(   | jjD| jE| j� tjFd2� Y nX �n�dd lG} |g}!| j|��r�tHjI}"|"j$� jJd3��rv|"d d=� |"d>d �  }"|"d6g|! }!d0|	k�r�|!j,|	� | jKd7| jL|!�� ytM|�}#W n tNtOfk
�r�   d}#Y nX | jP|!| jQ| jQ| jQ|d8�}$| jj$� d9k�r|#dk�r| j<j=|#�}%nd }%x4t;j;| j<jRgg g d�d �rN| j<jRjSd��sP �qW |$jT|%�\}&}'| j7jU|&� |'�r|| j>d:|'� |$jVjW�  |$jXjW�  |$jY}(|(�r�| j>d1|(� n
| jKd;� d S )?Nr   r   r   r�   r   zNo such CGI script (%r)z#CGI script is not a plain file (%r)z!CGI script is not executable (%r)ZSERVER_SOFTWAREZSERVER_NAMEzCGI/1.1ZGATEWAY_INTERFACEZSERVER_PROTOCOLZSERVER_PORTZREQUEST_METHODZ	PATH_INFOZPATH_TRANSLATEDZSCRIPT_NAME�QUERY_STRINGZREMOTE_ADDR�authorizationr	   Z	AUTH_TYPEZbasic�ascii�:ZREMOTE_USERzcontent-typeZCONTENT_TYPEzcontent-length�CONTENT_LENGTH�referer�HTTP_REFERER�acceptz	
 �   �,ZHTTP_ACCEPTz
user-agent�HTTP_USER_AGENTZcookiez, �HTTP_COOKIE�REMOTE_HOSTzScript output follows�+r   �=zCGI script exit status %#x�   zw.exer   r�   z-uzcommand: %s)�stdin�stdoutrk   �envZpostz%szCGI script exited OK)r�   r�   r�   r�   r�   r�   ����������)Zr�   r�   r)   r�   r�   r/   r�   r�   r�   r-   r   r�   �isfileZ	FORBIDDENr�   �	have_forkr�   r�   Zdeepcopy�environr[   Zserverr   r.   r$   r   r    r�   r�   r�   rw   r4   r5   r(   �base64�binasciir6   rW   Zdecodebytes�decodeZError�UnicodeErrorZget_content_typeZgetallmatchingheadersr_   �striprc   r�   Zget_all�
setdefaultrR   r�   ra   rO   r�   rB   rC   r�   �waitpid�selectr2   �readrD   �setuidr�   �dup2r�   �execveZhandle_errorZrequest�_exit�
subprocessrj   r�   r�   rf   Zlist2cmdliner+   �	TypeErrorr*   �Popen�PIPEZ_sockZrecvZcommunicaterY   rk   r   r�   �
returncode))r   �dir�restr/   �iZnextdirZnextrestZ	scriptdirr�   r�   ZscriptZ
scriptnameZ
scriptfileZispyr�   Zuqrestr�   r�   r�   Zlengthr�   r�   �lineZuaZcoZ
cookie_str�kZdecoded_queryri   r�   �pid�stsr  ZcmdlineZinterp�nbytes�p�datar�   rk   Zstatusr   r   r   r�   ;  s4   

























zCGIHTTPRequestHandler.run_cgiN)r   r   r   r?   r�   r�   Zrbufsizer�   r   r�   r�   r�   r�   r�   r   r   r   r   r     s   
	
zHTTP/1.0i�  r   c       	      C   s�   ||f}|| _ ||| ��j}|jj� }dt|� }t|j|d |d d�� y|j�  W n& tk
r|   td� tj	d� Y nX W d Q R X d S )Nz
 [+] CONECTADO A localhost:r   r   )r   r   z

 [+] Saindo .... 
[0m)
r.   r   Zgetsocknamer$   �printrh   Zserve_forever�KeyboardInterruptrj   �exit)	�HandlerClassZServerClassZprotocolr   �bindr   ZhttpdZsaZserve_messager   r   r   �test�  s    
r  Z__main__z--cgiZ
store_true)�action�helpz--bindz-bZADDRESS)�defaultZmetavarr  r   Zstorer�   )r  r  �typeZnargsr  )r  r   r  )4r{   �__all__Zemail.utilsrq   rU   Zhttp.clientr0   r�   r�   r�   r�   r�   r�   r   r
   rj   rp   Zurllib.parser�   r�   Zargparser  r   r  Zsleep�inputZportar|   r}   r   r   ZStreamRequestHandlerr   r   r�   r�   r�   r�   r   r  r   ZArgumentParserZparserZadd_argumentr$   r+   Z
parse_argsri   ZcgiZhandler_classr   r  r   r   r   r   �<module>   sp   	
 }  U
