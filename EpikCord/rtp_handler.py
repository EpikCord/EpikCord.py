"""
I have taken this directly from https://github.com/nickvsnetworking/pyrtp/.
If you're Nick reading this, I would like to thank you for this.
I have no idea how to handle RPT Packets/headers and for me to find something like this is very helpful.
Check out Nick's website @ https://nickvsnetworking.com.
Again, not at all my code, this is all Nicks.
I do realise that there is no License in his repository,
"""


def generate_rtp_packet(rtp_params, packet_vars):

    ##Example Usage:
    # payload = 'd5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5'
    # packet_vars = {'version' : 2, 'padding' : 0, 'extension' : 0, 'csi_count' : 0, 'marker' : 0, 'payload_type' : 8, 'sequence_number' : 306, 'timestamp' : 306, 'ssrc' : 185755418, 'payload' : payload}
    # GenerateRTPpacket(packet_vars)             #Generates hex to send down the wire

    # The first twelve octets are present in every RTP packet, while the list of CSRC identifiers is present only when inserted by a mixer.
    # Generate first byte of header as binary string:
    version = str(
        format(rtp_params["version"], "b").zfill(2)
    )  # RFC189 Version (Typically 2)
    padding = str(rtp_params["padding"])  # Padding (Typically false (0))
    extension = str(rtp_params["extension"])  # Extension - Disabled
    csi_count = str(
        format(rtp_params["csi_count"], "b").zfill(4)
    )  # Contributing Source Identifiers Count (Typically 0)
    byte1 = format(int((version + padding + extension + csi_count), 2), "x").zfill(
        2
    )  # Convert binary values to an int then format that as hex with 2 bytes of padding if requiredprint(byte1)

    # Generate second byte of header as binary string:
    marker = str(rtp_params["marker"])  # Marker (Typically false)
    payload_type = str(
        format(rtp_params["payload_type"], "b").zfill(7)
    )  # 7 bit Payload Type (From https://tools.ietf.org/html/rfc3551#section-6)
    byte2 = format(int((marker + payload_type), 2), "x").zfill(
        2
    )  # Convert binary values to an int then format that as hex with 2 bytes of padding if required

    sequence_number = format(rtp_params["sequence_number"], "x").zfill(
        4
    )  # 16 bit sequence number (Starts from a random position and incriments per packet)

    timestamp = format(rtp_params["timestamp"], "x").zfill(
        8
    )  # (Typically incrimented by the fixed time between packets)

    ssrc = str(
        format(rtp_params["ssrc"], "x").zfill(8)
    )  # SSRC 32 bits           (Typically randomly generated for each stream for uniqueness)

    payload = rtp_params["payload"]

    # print(packet)
    return byte1 + byte2 + sequence_number + timestamp + ssrc + payload


def decode_rtp_packet(packet_bytes):
    byte1 = format(int(packet_bytes[:2], 16), "b")
    byte2 = format(int(packet_bytes[2:4], 16), "b").zfill(8)
    return {
        "version": int(byte1[:2], 2),
        "padding": int(byte1[2:3]),
        "extension": int(byte1[3:4]),
        "csi_count": int(byte1[4:8], 2),
        "marker": int(byte2[:1]),
        "payload_type": int(byte2[1:8], 2),
        "sequence_number": int(str(packet_bytes[4:8]), 16),
        "timestamp": int(str(packet_bytes[8:16]), 16),
        "ssrc": int(str(packet_bytes[16:24]), 16),
        "payload": str(packet_bytes[24:])
    }
