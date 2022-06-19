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

    packet = byte1 + byte2 + sequence_number + timestamp + ssrc + payload
    # print(packet)
    return packet


def decode_rtp_packet(packet_bytes):
    ##Example Usage:
    # packet_bytes = '8008d4340000303c0b12671ad5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5'
    # rtp_params = DecodeRTPpacket(packet_bytes)
    # Returns dict of variables from packet (packet_vars{})
    packet_vars = {}
    byte1 = packet_bytes[0:2]  # Byte1 as Hex
    byte1 = int(byte1, 16)  # Convert to Int
    byte1 = format(byte1, "b")  # Convert to Binary
    packet_vars["version"] = int(byte1[0:2], 2)  # Get RTP Version
    packet_vars["padding"] = int(byte1[2:3])  # Get padding bit
    packet_vars["extension"] = int(byte1[3:4])  # Get extension bit
    packet_vars["csi_count"] = int(byte1[4:8], 2)  # Get RTP Version

    byte2 = packet_bytes[2:4]

    byte2 = int(byte2, 16)  # Convert to Int
    byte2 = format(byte2, "b").zfill(8)  # Convert to Binary
    packet_vars["marker"] = int(byte2[0:1])
    packet_vars["payload_type"] = int(byte2[1:8], 2)

    packet_vars["sequence_number"] = int(str(packet_bytes[4:8]), 16)

    packet_vars["timestamp"] = int(str(packet_bytes[8:16]), 16)

    packet_vars["ssrc"] = int(str(packet_bytes[16:24]), 16)

    packet_vars["payload"] = str(packet_bytes[24:])
    return packet_vars
